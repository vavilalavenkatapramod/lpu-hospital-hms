"""
Serializers for Appointment models
"""
from rest_framework import serializers
from .models import Appointment, AppointmentSlot
from accounts.serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    patient_details = UserSerializer(source='patient', read_only=True)
    doctor_details = UserSerializer(source='doctor', read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_id', 'patient_details',
            'doctor', 'doctor_id', 'doctor_details',
            'appointment_date', 'appointment_time', 'reason',
            'status', 'notes', 'cancellation_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class AppointmentSlotSerializer(serializers.ModelSerializer):
    """Serializer for AppointmentSlot model"""
    doctor_details = UserSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = AppointmentSlot
        fields = [
            'id', 'doctor', 'doctor_details', 'day_of_week',
            'start_time', 'end_time', 'is_available'
        ]
        read_only_fields = ['id']


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating appointment status"""
    
    class Meta:
        model = Appointment
        fields = ['status', 'notes', 'cancellation_reason']
