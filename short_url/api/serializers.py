from urllib.parse import urlparse

from rest_framework import serializers

from short_url.api.models import ShortUrl


class ShortUrlSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for one ShortUrl"""
    class Meta:
        model = ShortUrl
        fields = [
            'id',
            'target_url',
            'name',
            'short_url',
            'created_at',
            'updated_at'
        ]

    short_url = serializers.SerializerMethodField('get_short_url')

    def get_short_url(self, obj):
        """Get short url value"""
        url = self.context['request'].build_absolute_uri()
        result = urlparse(url)
        return f'{result.scheme}//{result.netloc}/{obj.name}'


class ShortUrlListSerializer(ShortUrlSerializer):
    """Serializer for list ShortUrl"""
    class Meta(ShortUrlSerializer.Meta):
        fields = [
            'id',
            'url',
            'target_url',
            'name',
            'short_url'
        ]
