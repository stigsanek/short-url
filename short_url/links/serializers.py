from urllib.parse import urlparse

from rest_framework import serializers

from short_url.links.models import Link


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for one Link"""
    class Meta:
        model = Link
        fields = [
            'id',
            'target_url',
            'uid',
            'custom_uid',
            'name',
            'click_count',
            'created_at',
            'updated_at',
            'link',
            'custom_link'
        ]
        read_only_fields = ['uid', 'click_count']

    link = serializers.SerializerMethodField('get_link')
    custom_link = serializers.SerializerMethodField('get_custom_link')

    def get_link(self, obj):
        """Get link"""
        return self._create_path(obj.uid)

    def get_custom_link(self, obj):
        """Get custom link"""
        if obj.custom_uid:
            return self._create_path(obj.custom_uid)

    def _create_path(self, value):
        """Create full url path"""
        url = self.context['request'].build_absolute_uri()
        result = urlparse(url)
        return f'{result.scheme}://{result.netloc}/{value}/'


class LinkListSerializer(LinkSerializer):
    """Serializer for list Link"""
    class Meta(LinkSerializer.Meta):
        fields = [
            'id',
            'url',
            'target_url',
            'link',
            'custom_link'
        ]
