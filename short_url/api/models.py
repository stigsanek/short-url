from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Url(models.Model):
    """URL model"""
    class Meta:
        verbose_name = _('ссылка')
        verbose_name_plural = _('ссылки')

    target_url = models.URLField(
        help_text=_('Целевая ссылка, на которую будет редирект')
    )
    uid = models.CharField(
        max_length=10,
        unique=True,
        help_text=_('Автогенерируемый идентификатор')
    )
    custom_uid = models.CharField(
        max_length=15,
        null=True,
        unique=True,
        help_text=_(
            'Дополнительный пользовательский идентификатор (опционально)'
        )
    )
    name = models.CharField(
        max_length=100,
        null=True,
        help_text=_('Имя ссылки (опционально)')
    )
    click_count = models.IntegerField(
        default=0,
        help_text=_('Количество переходов')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_('Пользователь')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Дата обновления')
    )

    def __str__(self):
        return self.uid
