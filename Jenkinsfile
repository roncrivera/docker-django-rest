#!groovy

DOCKER_IMAGE_VERSION = "${utcIso8601()}"
gitRepoUrl           = 'https://github.com/roncrivera/docker-django-gatekeeper.git'

node('docker') {
    ansiColor('xterm') {
        stage('Clean workspace') {
            deleteDir()
        }

        def DOCKER_NAMESPACE     = 'riverron'
        def DOCKER_IMAGE_NAME    = 'docker-django-gatekeeper'
        def DOCKER_TARGET_IMAGE  = "${DOCKER_NAMESPACE}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}"

        stage('Checkout code') {
            checkout([$class: 'GitSCM',
                branches: scm.branches,
                doGenerateSubmoduleConfigurations: false,
                extensions: [[$class: 'LocalBranch'], [$class: 'CleanCheckout']],
                submoduleCfg: [],
                userRemoteConfigs: [[credentialsId: 'pipeline-readonly', url: "${gitRepoUrl}"]]
            ])
        }

        try {
            notifyStash();
            withEnv(["DJANGO_TEST_RUN=1"]) {
                stage('Build Docker image') {
                    def dimg = docker.build("${DOCKER_TARGET_IMAGE}", "--no-cache .")

                    dimg.inside {
                        stage('Run unit tests') {
                            sh "coverage run gatekeeper/manage.py test gatekeeper -v2"
                        }

                        stage('Generate coverage report') {
                            sh "coverage xml"
                            stash name: 'coverage-report', includes: 'coverage.xml'
                        }
                    }

                    artifactoryDockerRegistry {
                        stage('Publish Docker image') {
                            dimg.push()
                            dimg.push('latest')
                        }
                    }

                    stage('Clean-up image') {
                        sh "docker rmi -f ${DOCKER_TARGET_IMAGE} || true"
                    }

                    currentBuild.result = 'SUCCESS'
                }
            }
        } catch (Exception err) {
            currentBuild.result = 'FAILURE'
        }
    }
}

node('linux && ansible') {
    def http_proxy    = 'http://10.192.116.73:8080'
    def https_proxy   = 'http://10.192.116.73:8080'
    def no_proxy      = 'internal-kubernetes-elb-tools-cluster-1234567890.eu-west-1.elb.amazonaws.com'
    def credentialsId = null

    stage('Checkout code') {
        checkout([$class: 'GitSCM',
            branches: scm.branches,
            doGenerateSubmoduleConfigurations: false,
            extensions: [[$class: 'LocalBranch'], [$class: 'CleanCheckout']],
            submoduleCfg: [],
            userRemoteConfigs: [[credentialsId: 'pipeline-readonly', url: "${gitRepoUrl}"]]
        ])

        unstash 'coverage-report'
        sonarQube {
            code_sources = '.'
            code_exclusions = 'gatekeeper/gatekeeper/static/**'
            python_coverage_report_path = 'coverage.xml'
        }
    }

    stage('Install k8s Tools') {
        kubectl_home = installTool "kubectl-1.9.1"
        helm_home = installTool "helm-2.7.2"
    }

    stage('Deploy to k8s cluster') {
        def branchName = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()

        tiller_namespace = branchName == 'master' ? 'gatekeeper-dev' : 'playground'

        credentialsId = "${tiller_namespace}-kubeconfig"

        withCredentials([[$class: "FileBinding", credentialsId: "${credentialsId}", variable: 'KUBECONFIG']]) {
            withEnv(["KUBECONFIG=${KUBECONFIG}", "http_proxy=${http_proxy}", "https_proxy=${https_proxy}", "no_proxy=${no_proxy}",
                "TILLER_NAMESPACE=${tiller_namespace}", "PATH=$PATH:${helm_home}:${kubectl_home}"])  {

                try {
                    if (branchName == "master") {
                        sh """
                            helm upgrade --install --set image.tag=${DOCKER_IMAGE_VERSION} --debug -f ./chart/values.development.yaml gatekeeper ./chart
                        """
                    } else {
                        sh """
                            helm upgrade --install --set image.tag=${DOCKER_IMAGE_VERSION} --debug -f ./chart/values.playground.yaml gatekeeper ./chart
                        """
                    }

                    currentBuild.result = 'SUCCESS'
                } catch (Exception err) {
                    currentBuild.result = 'FAILURE'
                }

                sh """
                    helm ls
                    kubectl get po
                """
            }
        }
    }

    notifyStash();
}
