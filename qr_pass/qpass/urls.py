from django.urls import path, re_path

from . import views
from .views import PhotoUpdateView

app_name = 'passes'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('get-qr/<int:id>/', views.get_qr, name='get_qr'),
    path('check/<str:key>/', views.check, name='check'),
    path('logs/', views.logs, name='logs'),
    re_path(r'add-photo/(?P<pk>[\d]+)/', PhotoUpdateView.as_view(
        success_url='/'), name='add_photo'),
    path('view-photo/<int:id>/', views.view_photo, name='view_photo'),
    path('view-all', views.all_with_photo, name='all_photo'),
]
