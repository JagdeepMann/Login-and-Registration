from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/register', views.register_user),
    path('users/login', views.authentication),
    path('success', views.success),
    path('users/logout', views.logout)
]