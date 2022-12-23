from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User"""
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as err:
            raise serializers.ValidationError(str(err))
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()

        return user
