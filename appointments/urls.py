"""
URL configuration for appointments app
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, AppointmentSlotViewSet

router = DefaultRouter()
router.register(r'', AppointmentViewSet, basename='appointment')

urlpatterns = [
    # Create endpoint - accessible at /api/appointments/create/
    path('create/', AppointmentViewSet.as_view({'post': 'create'}), name='appointment-create'),
    
    # List endpoint - accessible at /api/appointments/
    path('', AppointmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='appointment-list'),
    
    # Detail endpoints
    path('<int:pk>/', AppointmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='appointment-detail'),
    path('<int:pk>/confirm/', AppointmentViewSet.as_view({'post': 'confirm'}), name='appointment-confirm'),
    path('<int:pk>/cancel/', AppointmentViewSet.as_view({'post': 'cancel'}), name='appointment-cancel'),
    path('<int:pk>/complete/', AppointmentViewSet.as_view({'post': 'complete'}), name='appointment-complete'),
    path('upcoming/', AppointmentViewSet.as_view({'get': 'upcoming'}), name='appointment-upcoming'),
    path('today/', AppointmentViewSet.as_view({'get': 'today'}), name='appointment-today'),
    
    # Slots
    path('slots/', AppointmentSlotViewSet.as_view({'get': 'list', 'post': 'create'}), name='appointment-slot-list'),
    path('slots/<int:pk>/', AppointmentSlotViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='appointment-slot-detail'),
]
