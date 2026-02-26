"""
Serializers for Billing models
"""
from rest_framework import serializers
from .models import Invoice, Payment
from accounts.serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    
    class Meta:
        model = Payment
        fields = [
            'id', 'invoice', 'amount', 'payment_method',
            'transaction_id', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model"""
    patient_details = UserSerializer(source='patient', read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'patient', 'patient_details', 'appointment',
            'invoice_number', 'description', 'amount', 'tax',
            'discount', 'total_amount', 'status', 'payment_method',
            'payment_date', 'due_date', 'notes', 'payments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'invoice_number', 'total_amount', 'created_at', 'updated_at']


class InvoiceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating invoices"""
    
    class Meta:
        model = Invoice
        fields = [
            'patient', 'appointment', 'description', 'amount',
            'tax', 'discount', 'due_date', 'notes'
        ]
