from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from short_url.links import serializers
from short_url.links.models import Link
from short_url.links.utils import generate_uid


class LinkViewSet(ModelViewSet):
    """
    Views set for Link

    list: Returns link list
    create: Create link
    retrieve: Returns link
    update: Full update link
    partial_update: Partial update link
    delete: Delete link
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Link.objects.filter(user_id=self.request.user.pk).order_by('pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.LinkListSerializer

        return serializers.LinkSerializer

    def perform_create(self, serializer):
        uid = generate_uid()
        while Link.objects.filter(uid=uid).exists():
            uid = generate_uid()

        serializer.save(uid=uid, user=self.request.user)
