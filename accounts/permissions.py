from rest_framework.permissions import BasePermission
from accounts.models import User
class IsRegistrar(BasePermission):
    """
    Allows access only to authenticated users with ADMIN role.
    """
    message="only admin can access this"
    
    def has_permission(self, request, view):
        # check authentication
        if request.user.user_type == User.ADMIN :
            return True
       
        return False