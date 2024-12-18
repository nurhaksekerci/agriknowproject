# api/authentication.py (veya uygun başka bir dosya)

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class PhoneLoginBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            # Kullanıcıyı telefon numarasına göre buluyoruz
            user = get_user_model().objects.get(phone=phone)
        except ObjectDoesNotExist:
            return None

        # Eğer şifre doğrulama eklemek istiyorsanız, burayı kullanabilirsiniz
        # Ancak şifre kullanılmadığı için bu kısmı kaldırabilirsiniz
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
