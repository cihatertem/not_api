from django.urls import path, include
from . import views_cls
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('users', views_cls.UserViewSet, basename='users')
router.register('profile', views_cls.ProfileViewSet, basename='profile')
router.register('notes', views_cls.NotesViewSet, basename='notes')
router.register('categories', views_cls.CategoriesViewSet, basename='categories')

app_name = 'base'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/login', views_cls.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
