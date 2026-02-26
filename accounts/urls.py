"""
URL configuration for accounts app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, 
    ChangePasswordView, UserProfileView,
    home_page, login_page, register_page, 
    dashboard_page, appointments_page, 
    prescriptions_page, invoices_page
)

urlpatterns = [
    # API endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Page routes
    path('', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('appointments/', appointments_page, name='appointments'),
    path('prescriptions/', prescriptions_page, name='prescriptions'),
    path('billing/', invoices_page, name='invoices'),
    
    # Django auth views
    path('auth/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
