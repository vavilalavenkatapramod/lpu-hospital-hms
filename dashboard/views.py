"""
Dashboard views for HMS - Analytics and Statistics
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import render
from django.db import models
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.cache import cache
from accounts.models import User, Doctor, Patient
from appointments.models import Appointment
from billing.models import Invoice, Payment
from prescriptions.models import Prescription


class DashboardStatsView(APIView):
    """API endpoint for dashboard statistics with Redis caching"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Try to get from cache first
        cache_key = 'dashboard_stats'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            # Calculate statistics
            today = timezone.now().date()
            
            # User counts
            total_patients = User.objects.filter(role='patient').count()
            total_doctors = User.objects.filter(role='doctor').count()
            
            # Appointment statistics
            total_appointments = Appointment.objects.count()
            today_appointments = Appointment.objects.filter(appointment_date=today).count()
            pending_appointments = Appointment.objects.filter(status='pending').count()
            completed_appointments = Appointment.objects.filter(status='completed').count()
            
            # Revenue statistics
            total_revenue = Invoice.objects.filter(status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            today_revenue = Invoice.objects.filter(status='paid', payment_date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            pending_payments = Invoice.objects.filter(status='pending').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            
            # Prescription statistics
            total_prescriptions = Prescription.objects.count()
            
            cached_data = {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'total_appointments': total_appointments,
                'today_appointments': today_appointments,
                'pending_appointments': pending_appointments,
                'completed_appointments': completed_appointments,
                'total_revenue': float(total_revenue),
                'today_revenue': float(today_revenue),
                'pending_payments': float(pending_payments),
                'total_prescriptions': total_prescriptions,
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, cached_data, 300)
        
        return Response(cached_data)


class RevenueChartView(APIView):
    """API endpoint for revenue chart data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        
        # Get revenue by day for the last N days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        daily_revenue = []
        current_date = start_date
        
        while current_date <= end_date:
            day_revenue = Invoice.objects.filter(
                status='paid',
                payment_date__date=current_date
            ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            
            daily_revenue.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'revenue': float(day_revenue)
            })
            current_date += timedelta(days=1)
        
        return Response(daily_revenue)


class AppointmentsChartView(APIView):
    """API endpoint for appointments chart data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        days = int(request.query_params.get('days', 7))
        
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        daily_appointments = []
        current_date = start_date
        
        while current_date <= end_date:
            count = Appointment.objects.filter(appointment_date=current_date).count()
            daily_appointments.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'count': count
            })
            current_date += timedelta(days=1)
        
        return Response(daily_appointments)


class DoctorPerformanceView(APIView):
    """API endpoint for doctor performance metrics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        doctors = Doctor.objects.select_related('user').annotate(
            total_appointments=Count('user__doctor_appointments'),
            completed_appointments=Count('user__doctor_appointments', filter=models.Q(user__doctor_appointments__status='completed'))
        )
        
        performance = []
        for doctor in doctors:
            performance.append({
                'id': doctor.id,
                'name': f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
                'specialization': doctor.specialization,
                'total_appointments': doctor.total_appointments,
                'completed_appointments': doctor.completed_appointments,
            })
        
        return Response(performance)


class RecentActivityView(APIView):
    """API endpoint for recent activity"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get recent appointments
        recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]
        
        # Get recent payments
        recent_payments = Payment.objects.select_related('invoice__patient').order_by('-created_at')[:5]
        
        activity = {
            'appointments': [
                {
                    'id': apt.id,
                    'patient': f"{apt.patient.first_name} {apt.patient.last_name}",
                    'doctor': f"Dr. {apt.doctor.first_name} {apt.doctor.last_name}",
                    'date': apt.appointment_date.strftime('%Y-%m-%d'),
                    'time': apt.appointment_time.strftime('%H:%M'),
                    'status': apt.status,
                    'created_at': apt.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for apt in recent_appointments
            ],
            'payments': [
                {
                    'id': pay.id,
                    'patient': f"{pay.invoice.patient.first_name} {pay.invoice.patient.last_name}",
                    'amount': float(pay.amount),
                    'payment_method': pay.payment_method,
                    'created_at': pay.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for pay in recent_payments
            ]
        }
        
        return Response(activity)


# Django Views for HTML Pages
def dashboard_page(request):
    """Render dashboard page - routes to role-specific dashboard"""
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        from django.urls import reverse
        return redirect(reverse('login'))
    
    user = request.user
    
    # Route to role-specific dashboard
    if user.role == 'admin':
        return render(request, 'dashboard/dashboard.html', {'dashboard_type': 'admin'})
    elif user.role == 'doctor':
        return render(request, 'dashboard/doctor_dashboard.html', {'dashboard_type': 'doctor'})
    elif user.role == 'patient':
        return render(request, 'dashboard/patient_dashboard.html', {'dashboard_type': 'patient'})
    else:
        # Default to admin dashboard
        return render(request, 'dashboard/dashboard.html', {'dashboard_type': 'admin'})
