from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-auth', views.adminAuth, name='admin-authantication'),
    path('staff-auth', views.staffAuth, name='staff-authantication'),
    path('auth-forgot-password', views.varifyMail, name='auth-forgot-password'),
]
