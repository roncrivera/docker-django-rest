from rest_framework.permissions import BasePermission, SAFE_METHODS

safe_users = ['rundeck', 'ptpmain']

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # GET, HEAD, OPTIONS
            return True
        else:
            if request.user.is_active and request.user.username in safe_users and request.method == 'PUT':
                return True
            else:
                return request.user.is_staff
