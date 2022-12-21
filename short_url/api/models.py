from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class ShortUrl(models.Model):
    """URL model"""
    class Meta:
        verbose_name = _('ссылка')
        verbose_name_plural = _('ссылки')

    def __str__(self):
        return self.name

    target_url = models.CharField(
        max_length=200,
        verbose_name=_('целевая ссылка')
    )
    name = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('имя')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='user_links',
        null=True,
        verbose_name=_('пользователь')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('дата обновления')
    )
