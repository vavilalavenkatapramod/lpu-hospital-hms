"""
Serializers for Prescription models
"""
from rest_framework import serializers
from .models import Prescription, PrescriptionMedicine
from accounts.serializers import UserSerializer


class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    """Serializer for PrescriptionMedicine model"""
    
    class Meta:
        model = PrescriptionMedicine
        fields = [
            'id', 'medicine_name', 'dosage', 'frequency', 
            'duration', 'instructions', 'is_active'
        ]
        read_only_fields = ['id']


class PrescriptionSerializer(serializers.ModelSerializer):
    """Serializer for Prescription model"""
    patient_details = UserSerializer(source='patient', read_only=True)
    doctor_details = UserSerializer(source='doctor', read_only=True)
    medicines = PrescriptionMedicineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'appointment', 'patient', 'patient_details',
            'doctor', 'doctor_details', 'diagnosis', 'symptoms',
            'notes', 'follow_up_date', 'is_active', 'medicines',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PrescriptionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating prescription with medicines"""
    medicines = PrescriptionMedicineSerializer(many=True)
    
    class Meta:
        model = Prescription
        fields = [
            'appointment', 'patient', 'doctor', 'diagnosis',
            'symptoms', 'notes', 'follow_up_date', 'medicines'
        ]
    
    def create(self, validated_data):
        medicines_data = validated_data.pop('medicines')
        prescription = Prescription.objects.create(**validated_data)
        for medicine_data in medicines_data:
            PrescriptionMedicine.objects.create(prescription=prescription, **medicine_data)
        return prescription
