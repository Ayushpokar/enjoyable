# authentication_backends.py
from django.contrib.auth.backends import ModelBackend
from .models import user_master
from django.contrib.auth.hashers import check_password

class CustomBackend(ModelBackend):
    def authenticate(self,request, username=None, password=None):
        try:
            user = user_master.objects.get(username=username)
            if check_password(password, user.password):
                return user
        except user_master.DoesNotExist:
            return print("user does not exist. Please register")
