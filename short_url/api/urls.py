from django.urls import include, path
from rest_framework.routers import DefaultRouter

from short_url.api import views

router = DefaultRouter()
router.register(r'urls', views.UrlViewSet, basename='url')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', views.CreateUserView.as_view())
]
