"""short_url URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

from short_url.links.views import LinkViewSet
from short_url.users.views import CustomAuthToken, UserViewSet

router = SimpleRouter()
router.register(r'links', LinkViewSet, basename='link')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('openapi/', get_schema_view(
        title="Short URL API",
        description="API service for URL shortening",
        public=True,
        version="v1"
    ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    )),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    )),
    path('api/', include(router.urls)),
    path('api/auth-token/', CustomAuthToken.as_view(), name='auth-token'),
    path('admin/', admin.site.urls)
]
