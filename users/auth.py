from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None,username=None, password=None, **kwargs):
        UserModel = get_user_model()
        print("Calling",username,email)
        try:
            if email:
                user = UserModel.objects.get(email=email)
            elif username:
                user = UserModel.objects.get(username=username)
            print(user)
        except UserModel.DoesNotExist:
            return None
        else:
            print(user)
            if user.check_password(password):
                return user
        return None
