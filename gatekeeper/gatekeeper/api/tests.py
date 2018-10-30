from django.test import TestCase
from gatekeeper.main.models import Deployment
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


# Create your tests here.
class ViewTestCase(TestCase):
    """Test suite for the API views."""

    def setUp(self):
        """Define the API client and test variables."""
        self.client = APIClient()
        self.jira_ticket = 'PTP-123'
        self.assignee_bank_id = 123456
        self.artifact_path = 'generic-production/riverron/gatekeeper.tar.gz'
        self.remedy_cr_number = 'INC-1'
        self.rundeck_job_id = 'b2028af6-8630-4463-aea7-b6b3c71b2f1b'
        self.rundeck_log_url = 'http://rundeck/job/log/url'
        self.deployment = {
            'jira_ticket': self.jira_ticket,
            'assignee_bank_id': self.assignee_bank_id,
            'artifact_path': self.artifact_path,
            'remedy_cr_number': self.remedy_cr_number,
            'rundeck_job_id': self.rundeck_job_id,
        }
        self.response = self.client.post(
            reverse('create'),
            self.deployment,
            format="json"
        )

    def test_api_can_create_a_deployment(self):
        """Test the API can create a deployment object."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_deployment(self):
        """Test the API can get a given deployment."""
        deployment = Deployment.objects.get(jira_ticket=self.jira_ticket)
        response = self.client.get(
            reverse('details',
            kwargs={'jira_ticket': deployment.jira_ticket}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, deployment)

    def test_api_can_update_a_deployment_with_rundeck_payload(self):
        """Test the API can update a given deployment with rundeck payload."""
        deployment = Deployment.objects.get(jira_ticket=self.jira_ticket)
        rundeck_payload = {
            'rundeck_log_url': self.rundeck_log_url,
            'rundeck_status': 'succeeded',
        }
        res = self.client.put(
            reverse('details', kwargs={'jira_ticket': deployment.jira_ticket}),
            rundeck_payload, format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
