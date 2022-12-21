from rest_framework import viewsets

from short_url.api.models import ShortUrl
from short_url.api.serializers import ShortUrlSerializer


class ShortUrlViewSet(viewsets.ModelViewSet):
    """Views set for ShortUrl"""
    serializer_class = ShortUrlSerializer

    def get_queryset(self):
        """Filters data for the current user"""
        return ShortUrl.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
