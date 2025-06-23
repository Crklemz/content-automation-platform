from django.urls import path
from .views import site_config_list

urlpatterns = [
    path('', site_config_list),
]
