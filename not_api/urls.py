from django.contrib import admin
from django.urls import path, include
from os import getenv
from dotenv import load_dotenv

load_dotenv()

admin_url = 'admin/' if getenv("DEBUG") == "True" else getenv('ADMIN_ADDRESS')

urlpatterns = [
    path(admin_url, admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('note_app/', include(('base.urls_cls', 'base'), namespace='class_based')) \
        if getenv('VIEW_BASED') == 'CLASS' \
        else path('note_app/', include(('base.urls', 'base'), namespace='func_based')),
]
