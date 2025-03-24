from django.urls import path, include
from users.views import UserViewSet, RegisterViewSet , ProfileViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegisterViewSet, basename='register')
router.register('profile', ProfileViewSet, basename='profile')


urlpatterns = [
    path("", include(router.urls))
]
