from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from short_url.links.models import Link


@require_http_methods(['GET'])
def redirect_view(request, slug):
    """View for redirect to target url"""
    link = get_object_or_404(Link, Q(uid=slug) | Q(custom_uid=slug))
    link.click_count += 1
    link.save()

    return redirect(link.target_url)
