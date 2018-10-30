# Django
from django.urls import path, include, re_path
from .views import CreateView, DetailsView

# Django REST Framework
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

schema_view = get_schema_view(title='Gatekeeper API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = {
    path(r'api/docs/', schema_view, name="docs"),
    path(r'api/v1/deployments/', CreateView.as_view(), name="create"),
    re_path(r'api/v1/deployments/(?P<jira_ticket>[\w-]+)/', DetailsView.as_view(), name="details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
