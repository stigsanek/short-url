from django.urls import include, path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import SimpleRouter

from short_url.api import views

router = SimpleRouter()
router.register(r'urls', views.UrlViewSet, basename='url')

urlpatterns = [
    path('', include(router.urls)),
    path('auth-token/', ObtainAuthToken.as_view()),
    path('users/', views.CreateUserView.as_view())
]
