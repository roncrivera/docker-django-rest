from django.test import TestCase
from .models import Deployment


# Create your tests here.
class ModelTestCase(TestCase):
    """This class defines the test suite for the model."""

    def setUp(self):
        """Define the test client and test variables."""
        self.jira_ticket = 'PTP-123'
        self.assignee_bank_id = 123456
        self.artifact_path = 'generic-production/riverron/gatekeeper.tar.gz'
        self.remedy_cr_number = 'INC-1'
        self.rundeck_job_id = 'b2028af6-8630-4463-aea7-b6b3c71b2f1b'
        self.deployment = {
            'jira_ticket': self.jira_ticket,
            'assignee_bank_id': self.assignee_bank_id,
            'artifact_path': self.artifact_path,
            'remedy_cr_number': self.remedy_cr_number,
            'rundeck_job_id': self.rundeck_job_id,
        }

    def test_model_can_create_a_deployment(self):
        """Test the model can create a deployment object."""
        old_count = Deployment.objects.count()
        self.deployment = Deployment(**self.deployment)
        self.deployment.save()
        new_count = Deployment.objects.count()
        self.assertNotEqual(old_count, new_count)
