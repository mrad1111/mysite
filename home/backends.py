from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate
    using either their username OR their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        # Search for user by username or email (case-insensitive)
        user = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
