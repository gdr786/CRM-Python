from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-auth', views.adminAuth, name='admin-authantication'),
    path('staff-auth', views.staffAuth, name='staff-authantication'),
    path('auth-forgot-password/<str:type>', views.varifyMail, name='auth-forgot-password'),
    path('forgot-password-step/<str:type>', views.forgetPassStep, name='forget-password-step'),
    path('resend-otp-mail/<str:type>', views.resendOtpMail, name='resend-otp-mail'),
    path('change-password/<str:type>', views.changePassword, name='change-password'),
]
