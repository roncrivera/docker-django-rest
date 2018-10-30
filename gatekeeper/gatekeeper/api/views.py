# Python
import os
import logging
import requests
import json
from pathlib import Path

# Django
from gatekeeper.main.models import Deployment

# Django REST Framework
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# API
from gatekeeper.api.serializers import DeploymentSerializer, DeploymentUpdateSerializer
from gatekeeper.api.rundeck_scb import Rundeck
from gatekeeper.api.permissions import IsAdminOrReadOnly

# Environment variables
PTP_URL = os.environ.get('MAIN_URL')


base_dir = Path(__file__).parents[3]
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', filename='%s/application.log' % base_dir, level=logging.INFO)
logger = logging.getLogger(__name__)


# Create your views here.
def trigger_rundeck_job(deployment, arg_string):
    jira_ticket = deployment.jira_ticket
    bank_id = str(deployment.assignee_bank_id)
    job_id = deployment.rundeck_job_id
    rundeck = Rundeck()

    try:
        rundeck.generate_token(user_id=bank_id, roles=bank_id, duration="2h")
        logger.info("%s Rundeck generate token response:\n%s" % (jira_ticket, rundeck.generate_token_response.content))
        auth_token = rundeck.generate_token_response.json()['token']
        rundeck.trigger_job(job_id=job_id, argString=arg_string, auth_token=auth_token)
        logger.info("%s Rundeck job response:\n%s" % (jira_ticket, rundeck.job_response.content))
        job_response = json.loads(rundeck.job_response.content.decode())

        if 'error' in job_response and job_response['error']:
            payload = {"status": 'FAILED', "job_response": job_response}
            send_deployment_status(jira_ticket, payload)
    except Exception as e:
        logger.critical("%s: An exception occurred sending Rundeck deployment request\n%s" % (jira_ticket, str(e)))
        raise
    else:
        deployment.status = 'request sent to Rundeck'
        deployment.save()
        logger.info("%s Submitted Rundeck deployment request" % jira_ticket)


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our REST api."""
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def perform_create(self, serializer):
        """Save the post data when creating a new deployment."""
        serializer.save(status='pending')

        deployment = Deployment.objects.get(jira_ticket=self.request.data['jira_ticket'])
        rundeck_args = "-RemedyTicketNumber {} -jira_ticket {} -artifactPack {}".format(deployment.remedy_cr_number, deployment.jira_ticket, deployment.artifact_path)

        try:
            if not os.environ.get('DJANGO_TEST_RUN'):
                trigger_rundeck_job(deployment, rundeck_args)
        except Exception as e:
            logger.critical("%s Rundeck deployment request failed\n%s" % (deployment.jira_ticket, str(e)))
            raise


def send_deployment_status(jira_ticket, payload):
    headers = {}
    headers['Content-Type'] = 'application/json'
    url = "{}/deploy/update/{}".format(PTP_URL, jira_ticket)

    try:
        response = requests.post(url=url, json=payload, headers=headers)
    except Exception as e:
        logger.critical("%s Deployment status update failed\n%s" % (jira_ticket, str(e)))
        raise
    else:
        logger.info("%s Deployment status update sent to PTP" % jira_ticket)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the HTTP GET, PUT and DELETE requests."""

    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    update_serializer_class = DeploymentUpdateSerializer
    permission_classes = (IsAdminOrReadOnly, )

    lookup_field = 'jira_ticket'

    def get_serializer_class(self):
        """Return a different serializer if performing an update."""
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' and self.update_serializer_class:
            serializer_class = self.update_serializer_class

        return serializer_class

    def perform_update(self, serializer):
        """Save the put data when updating a deployment."""
        serializer.save()
        jira_ticket = serializer.data['jira_ticket']
        logger.info("%s Updated with payload %r" % (jira_ticket, self.request.data))

        deployment = Deployment.objects.get(jira_ticket=jira_ticket)
        payload = {"status": deployment.rundeck_status, "rundeck_log_url": deployment.rundeck_log_url, "artifact_path": deployment.artifact_path}

        try:
            if not os.environ.get('DJANGO_TEST_RUN'):
                send_deployment_status(jira_ticket, payload)
        except Exception as e:
            logger.critical("%s Sending deployment status to PTP failed\n%s" % (jira_ticket, str(e)))
            raise
        else:
            deployment.status = deployment.rundeck_status
            deployment.save()
