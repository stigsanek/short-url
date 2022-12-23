from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from short_url.users import serializers


class CustomAuthToken(ObtainAuthToken):
    """Custom ObtainAuthToken"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk
        })


class UserViewSet(ModelViewSet):
    """Views set for Link"""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
