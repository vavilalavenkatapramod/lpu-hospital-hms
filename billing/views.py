"""
Billing views for HMS
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Sum, Q
from datetime import datetime, date
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, InvoiceCreateSerializer, PaymentSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Invoice CRUD operations"""
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Invoice.objects.all().select_related('patient', 'appointment')
        elif user.role == 'doctor':
            return Invoice.objects.filter(appointment__doctor=user).select_related('patient', 'appointment')
        elif user.role == 'patient':
            return Invoice.objects.filter(patient=user).select_related('patient', 'appointment')
        return Invoice.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceCreateSerializer
        return InvoiceSerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.role not in ['admin', 'doctor']:
            return Response(
                {'error': 'Only doctors and admins can create invoices'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """Mark invoice as paid"""
        invoice = self.get_object()
        invoice.status = 'paid'
        invoice.payment_method = request.data.get('payment_method', 'online')
        invoice.payment_date = datetime.now()
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an invoice"""
        invoice = self.get_object()
        invoice.status = 'cancelled'
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending invoices"""
        invoices = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def paid(self, request):
        """Get paid invoices"""
        invoices = self.get_queryset().filter(status='paid')
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment CRUD operations"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.all().select_related('invoice')
        elif user.role == 'patient':
            return Payment.objects.filter(invoice__patient=user).select_related('invoice')
        return Payment.objects.none()


# Django Views for HTML Pages
def invoices_page(request):
    """Render invoices page"""
    return render(request, 'billing/invoices.html')


def invoice_detail_page(request, invoice_id):
    """Render invoice detail page"""
    return render(request, 'billing/invoice_detail.html', {'invoice_id': invoice_id})
