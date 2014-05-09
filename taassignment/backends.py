import ldap
from djangocas.backends import CASBackend
from taassignment.users.models import User 
from django.conf import settings
from django.core.exceptions import PermissionDenied

class PSUBackend(CASBackend):
    def get_or_init_user(self, username):
        try:
            user = User.objects.get(username=username)

            # TA login, they also get permission denied.
            if user.is_ta and not user.is_staff and not user.is_faculty:
                return None
            
        except User.DoesNotExist:
            return None

        return user