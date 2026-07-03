from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsWorker(BasePermission):
    """
    Allows access only to worker users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'worker')

class IsAdminOrAuthenticatedReadOnly(BasePermission):
    """
    Allows read-only access to authenticated users, but write access only to admin users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True # Allow read-only access for all authenticated users
        
        # Write permissions are only allowed to admin users.
        return request.user.role == 'admin'
