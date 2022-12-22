from rest_framework import viewsets

from short_url.api import serializers
from short_url.api.models import Url


class UrlViewSet(viewsets.ModelViewSet):
    """Views set for Url"""

    def get_queryset(self):
        return Url.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UrlListSerializer

        return serializers.UrlSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
