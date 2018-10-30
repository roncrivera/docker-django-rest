from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
class Deployment(models.Model):
    """This class represents the Deployment model."""
    jira_ticket = models.CharField(max_length=255, unique=True)
    artifact_path = models.CharField(max_length=255)
    assignee_bank_id = models.IntegerField()
    remedy_cr_number = models.CharField(max_length=255)
    rundeck_job_id = models.CharField(max_length=255)
    rundeck_log_url = models.CharField(max_length=255, blank=True, null=True)
    rundeck_status = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.jira_ticket)
