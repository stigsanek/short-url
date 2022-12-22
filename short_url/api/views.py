from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from short_url.api import serializers
from short_url.api.models import Url
from short_url.api.utils import generate_uid


class UrlViewSet(ModelViewSet):
    """Views set for Url"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Url.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UrlListSerializer

        return serializers.UrlSerializer

    def perform_create(self, serializer):
        uid = generate_uid()
        while Url.objects.filter(uid=uid).exists():
            uid = generate_uid()

        serializer.save(uid=uid, user=self.request.user)


class CreateUserView(CreateAPIView):
    """Views set for create User"""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
