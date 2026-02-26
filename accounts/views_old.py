"""
Authentication views for HMS
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Doctor, Patient
from .serializers import (
    UserSerializer, RegisterSerializer, DoctorSerializer, 
    PatientSerializer, LoginSerializer, ChangePasswordSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create associated profile based on role
        if user.role == 'doctor':
            Doctor.objects.create(user=user)
        elif user.role == 'patient':
            Patient.objects.create(user=user)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """API endpoint for user login"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user is None:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'User account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class LogoutView(APIView):
    """API endpoint for user logout"""
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'})
        except Exception:
            return Response({'message': 'Logout successful'})


class ChangePasswordView(generics.UpdateAPIView):
    """API endpoint for changing password"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint for user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


# Django Views for HTML Pages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def login_page(request):
    """Render login page and handle login"""
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    
    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')
        
        user = None
        
        # Since USERNAME_FIELD = 'email', authenticate with email
        if '@' in login_input:
            # It's an email
            user = authenticate(request, email=login_input, password=password)
        else:
            # It's a username - first try username, then check if it's an email
            user = authenticate(request, username=login_input, password=password)
            
            # If that fails, try to find user by email
            if user is None:
                try:
                    user_obj = User.objects.get(email=login_input)
                    user = authenticate(request, email=user_obj.email, password=password)
                except User.DoesNotExist:
                    user = None
        
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username/email or password'})
    
    return render(request, 'accounts/login.html')


def register_page(request):
    """Render registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return render(request, 'accounts/register.html')


def home_page(request):
    """Render home page"""
    return render(request, 'home.html')


def dashboard_page(request):
    """Render dashboard page"""
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    return render(request, 'dashboard/dashboard.html')


def appointments_page(request):
    """Render appointments page"""
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    return render(request, 'appointments/appointments.html')


def prescriptions_page(request):
    """Render prescriptions page"""
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    return render(request, 'prescriptions/prescriptions.html')


def invoices_page(request):
    """Render invoices page"""
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    return render(request, 'billing/invoices.html')
