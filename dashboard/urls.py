from django.urls import path
from . import views
from community import views as community_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/users/export/', views.export_users_csv, name='export_users_csv'),
    path('notifications/', views.notifications, name='notifications'),
    path('achievements/', views.achievements, name='achievements'),
    path('checkin/', views.daily_checkin, name='daily_checkin'),
    path('paths/', views.ai_paths, name='ai_paths'),
    path('paths/join/<int:path_id>/', views.join_path, name='join_path'),
    
    # Community
    path('community/', community_views.community_home, name='community'),
    path('community/<slug:channel_slug>/', community_views.community_home, name='community_channel'),
    path('community/<slug:channel_slug>/send/', community_views.send_message, name='send_message'),
    path('community/<slug:channel_slug>/messages/', community_views.get_messages, name='get_messages'),
]
