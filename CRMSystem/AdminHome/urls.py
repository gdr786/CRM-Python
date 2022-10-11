from django.urls import path, include
from . import views

urlpatterns = [
    path('check/<admin_id>/', views.checkUser, name='checkuser'),
    path('admin-home', views.home, name='dashboard'),
]
