from django.urls import path

from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/edit', views.edit, name='edit'),
    path('<int:article_id>/comments', views.comments, name='comments'),
]