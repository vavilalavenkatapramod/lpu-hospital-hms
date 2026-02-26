"""
Appointment views for HMS
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q
from .models import Appointment, AppointmentSlot
from .serializers import (
    AppointmentSerializer, AppointmentSlotSerializer, 
    AppointmentUpdateSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read-only access for authenticated users, write only for admin"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Appointment CRUD operations"""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Appointment.objects.all().select_related('patient', 'doctor')
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor=user).select_related('patient', 'doctor')
        elif user.role == 'patient':
            return Appointment.objects.filter(patient=user).select_related('patient', 'doctor')
        return Appointment.objects.none()
    
    def create(self, request, *args, **kwargs):
        # Patients can only create appointments for themselves
        if request.user.role == 'patient':
            request.data['patient'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Only doctors and admins can update appointments
        if request.user.role not in ['admin', 'doctor']:
            return Response(
                {'error': 'You do not have permission to update appointments'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm an appointment"""
        appointment = self.get_object()
        if request.user.role not in ['admin', 'doctor'] or appointment.doctor != request.user:
            return Response(
                {'error': 'You do not have permission to confirm this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        appointment.status = 'confirmed'
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        if request.user.role not in ['admin', 'patient'] and appointment.patient != request.user:
            return Response(
                {'error': 'You do not have permission to cancel this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        appointment.status = 'cancelled'
        appointment.cancellation_reason = request.data.get('reason', '')
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark appointment as completed"""
        appointment = self.get_object()
        if request.user.role not in ['admin', 'doctor'] or appointment.doctor != request.user:
            return Response(
                {'error': 'You do not have permission to complete this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        appointment.status = 'completed'
        appointment.notes = request.data.get('notes', '')
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments"""
        from django.utils import timezone
        from datetime import datetime, date
        
        today = date.today()
        appointments = self.get_queryset().filter(
            Q(appointment_date__gte=today) &
            Q(status__in=['pending', 'confirmed'])
        )
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments"""
        from django.utils import timezone
        from datetime import date
        
        today = date.today()
        appointments = self.get_queryset().filter(appointment_date=today)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)


class AppointmentSlotViewSet(viewsets.ModelViewSet):
    """ViewSet for AppointmentSlot CRUD operations"""
    serializer_class = AppointmentSlotSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return AppointmentSlot.objects.all().select_related('doctor')
        elif user.role == 'doctor':
            return AppointmentSlot.objects.filter(doctor=user)
        return AppointmentSlot.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'doctor':
            serializer.save(doctor=self.request.user)
        else:
            serializer.save()


# Django Views for HTML Pages
def appointments_page(request):
    """Render appointments page"""
    return render(request, 'appointments/appointments.html')


def book_appointment_page(request):
    """Render book appointment page"""
    return render(request, 'appointments/book_appointment.html')
