from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'base'

urlpatterns = [
    path('api', views.get_routes, name='routes'),
    path('api/token/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users', views.create_user, name='create_user'),
    path('api/profile', views.profile_handler, name='profile'),
    path('api/notes', views.note_list, name='notes'),
    path('api/notes/<str:note_id>', views.single_note, name='note'),
    path('api/categories', views.category_list, name='categories'),
    path('api/categories/<str:category_id>', views.single_category, name='category'),
    path('api/categories/<str:category_id>/notes', views.category_notes, name='category_notes'),
]
