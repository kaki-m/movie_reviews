from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except:
            print('backends.pyでget_userに失敗しました')
            return None