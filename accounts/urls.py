from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('admin-dashboard', views.adminDashboard, name="adminDashboard"),
    path('dashboard-uploader', views.dashboardUploader, name="dashboardUploader"),
    path('dashboard-uploader-history', views.dashboardUploaderHistory, name="dashboardUploaderHistory"),
    path('upload', views.upload, name="upload"),
    path('adduser', views.adduser, name="adduser"),
    path('download/<slug:file_id>', views.download, name='download'),  
]