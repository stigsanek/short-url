from django.contrib import admin

from short_url.api.models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = (
        'target_url', 'name', 'user', 'created_at', 'updated_at'
    )
    list_filter = ('user',)
    search_fields = ('name',)
