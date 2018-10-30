# Django
from gatekeeper.main.models import Deployment

# Django REST Framework
from rest_framework import serializers


class DeploymentSerializer(serializers.ModelSerializer):
    """Serializer to map the Deployment instance into JSON format."""

    class Meta:
        """Meta class to map serializer's field with the model fields."""
        model = Deployment
        fields = '__all__'
        read_only_fields = ('date_created', 'date_modified')


class DeploymentUpdateSerializer(serializers.ModelSerializer):
    """Serializer to map the Deployment instance into JSON format."""

    class Meta:
        """Meta class to map serializer's field with the model fields."""
        model = Deployment
        fields = '__all__'
        read_only_fields = ('jira_ticket', 'assignee_bank_id', 'artifact_path', 'remedy_cr_number', 'rundeck_job_id', 'status', 'date_created', 'date_modified')
