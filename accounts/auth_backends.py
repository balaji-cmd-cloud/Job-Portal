from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # The 'username' parameter holds the email value in our configuration
        email = username or kwargs.get('email')
        UserModel = get_user_model()
        if email is None:
            return None
        try:
            # Case-insensitive email lookups
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
