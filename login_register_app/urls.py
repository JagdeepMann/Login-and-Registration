from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/register', views.register_user),
    path('users/login', views.authentication),
    path('success', views.success),
    path('users/logout', views.logout),
    
    path('post_message', views.post_message),
    path('post_comment', views.post_comment),
    path('delete_message', views.delete_message),
    path('delete_comment', views.delete_comment),
]