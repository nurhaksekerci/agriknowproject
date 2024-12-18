from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

class CustomTokenObtainPair(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # İlk başta gelen GET isteğine varsayılan boş JSON döndürüyoruz
        return Response({
            "phone": ""
        }, status=status.HTTP_200_OK)

    def post(self, request):
        phone = request.data.get('phone')

        if not phone:
            raise AuthenticationFailed('Telefon numarası gerekli')

        # Telefon numarasına dayalı kullanıcıyı buluyoruz
        user = get_user_model().objects.filter(phone=phone).first()

        if not user:
            raise AuthenticationFailed('Telefon numarasıyla ilişkilendirilmiş bir kullanıcı bulunamadı')

        # RefreshToken oluşturuyoruz
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token,
            'refresh': str(refresh),
            'phone': user.phone
        }, status=status.HTTP_200_OK)
