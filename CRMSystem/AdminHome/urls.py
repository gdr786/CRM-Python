from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

# for files

urlpatterns = [
    path('check/<admin_id>/', views.checkUser, name='checkuser'),
    path('admin-home', views.home, name='dashboard'),
    path('admin-list', views.adminList, name='admin-list'),
    path('add-admin', views.addAdmin, name='add-admin'),
    path('edit-admin/<id>/<str:type>', views.addAdmin, name='edit-admin'),
    path('delete-admin/<id>/<str:type>', views.addAdmin, name='delete-admin'),
    path("logout", views.logout, name="logout")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# only in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
