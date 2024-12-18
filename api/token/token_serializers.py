from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, default="")  # Varsayılan değer ekleyin

    def validate(self, attrs):
        phone = attrs.get('phone')

        # Telefon numarasına dayalı kullanıcıyı buluyoruz
        user = get_user_model().objects.filter(phone=phone).first()

        if not user:
            raise AuthenticationFailed('Telefon numarasıyla ilişkilendirilmiş bir kullanıcı bulunamadı')

        # RefreshToken oluşturuyoruz
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return {
            'access': access_token,
            'refresh': str(refresh),
            'phone': user.phone  # Kullanıcı bulunduğunda telefon numarasını döndürüyoruz
        }
