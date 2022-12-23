from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
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
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action == 'create' and self.request.method == 'POST':
            return super().get_permissions()

        return [IsAuthenticated()]

    def perform_update(self, serializer):
        if self.request.user.id != self.kwargs.get('pk'):
            raise PermissionDenied(
                _('You have no rights to change another user')
            )

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.id != self.kwargs.get('pk'):
            raise PermissionDenied(
                _('You do not have permission to delete another user')
            )

        instance.delete()
