from urllib.parse import urlparse

from rest_framework import serializers

from short_url.api.models import ShortUrl


class ShortUrlSerializer(serializers.HyperlinkedModelSerializer):
    """ShortUrl serializer"""
    class Meta:
        model = ShortUrl
        fields = [
            'id',
            'url',
            'target_url',
            'name',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        url = urlparse(data['url'])
        data['short_url'] = f"{url.scheme}//{url.netloc}/{data['name']}"
        return data
