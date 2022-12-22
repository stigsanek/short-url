from rest_framework import viewsets

from short_url.api import serializers
from short_url.api.models import Url
from short_url.api.utils import generate_uid


class UrlViewSet(viewsets.ModelViewSet):
    """Views set for Url"""

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
