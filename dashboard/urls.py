"""
URL configuration for dashboard app
"""
from django.urls import path
from .views import (
    DashboardStatsView, RevenueChartView, AppointmentsChartView,
    DoctorPerformanceView, RecentActivityView, dashboard_page
)

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('revenue-chart/', RevenueChartView.as_view(), name='revenue_chart'),
    path('appointments-chart/', AppointmentsChartView.as_view(), name='appointments_chart'),
    path('doctor-performance/', DoctorPerformanceView.as_view(), name='doctor_performance'),
    path('recent-activity/', RecentActivityView.as_view(), name='recent_activity'),
    path('', dashboard_page, name='dashboard'),
]
