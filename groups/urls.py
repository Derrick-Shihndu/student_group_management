from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.home, name='home'),
    path('admin-unlock/', views.admin_unlock, name='admin_unlock'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('confirm-reset/', views.confirm_reset, name='confirm_reset'),
    path('class/<int:pk>/', views.class_detail, name='class_detail'),
    path('class/<int:pk>/register/', views.register, name='register'),
    path('class/<int:pk>/post-note/', views.post_note, name='post_note'),
    path('class/<int:pk>/post-message/', views.post_message, name='post_message'),
    path('class/<int:pk>/select-leader/<int:sg_pk>/', views.select_leader, name='select_leader'),
]
