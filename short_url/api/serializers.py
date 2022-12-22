from urllib.parse import urlparse

from django.contrib.auth.models import User
from rest_framework import serializers

from short_url.api.models import Url


class UrlSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for one Url"""
    class Meta:
        model = Url
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
        return f'{result.scheme}://{result.netloc}/{value}'


class UrlListSerializer(UrlSerializer):
    """Serializer for list Url"""
    class Meta(UrlSerializer.Meta):
        fields = [
            'id',
            'url',
            'target_url',
            'link',
            'custom_link'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User"""
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
