from django.contrib import admin

from short_url.links.models import Link


@admin.register(Link)
class UrlAdmin(admin.ModelAdmin):
    list_display = (
        'target_url', 'name', 'user', 'created_at', 'updated_at'
    )
    list_filter = ('user',)
    search_fields = ('name',)
