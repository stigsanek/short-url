from rest_framework import viewsets

from short_url.api import serializers
from short_url.api.models import ShortUrl


class ShortUrlViewSet(viewsets.ModelViewSet):
    """Views set for ShortUrl"""

    def get_queryset(self):
        return ShortUrl.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ShortUrlListSerializer

        return serializers.ShortUrlSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
