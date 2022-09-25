from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, LogViewSet, get_qr, check

router_v1 = DefaultRouter()
router_v1.register('customer', CustomerViewSet)
router_v1.register('log', LogViewSet)

urlpatterns = [
    path('qr/get-qr/<int:id>/', get_qr),
    path('qr/check/<str:key>/', check),
    path('qr/', include(router_v1.urls)),
]
