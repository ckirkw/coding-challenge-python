from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login0, name='login'),
    path('logout', views.logout0, name='logout')
]