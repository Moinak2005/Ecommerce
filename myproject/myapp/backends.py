from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            # Check if the user exists by username or email
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
            if not user:
                raise User.DoesNotExist
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            User().set_password(password)
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
