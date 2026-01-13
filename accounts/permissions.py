from rest_framework.permissions import BasePermission
from accounts.models import User
class IsRegistrar(BasePermission):
    """
    Allows access only to authenticated users with a specific role.
    """
    message="only regitrar can access this"
    
    def has_permission(self, request, view):
        # check authentication
        if request.user.user_type == User.REGISTRAR :
            return True
       
        return False