"""
Prescription views for HMS
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Prescription, PrescriptionMedicine
from .serializers import PrescriptionSerializer, PrescriptionCreateSerializer, PrescriptionMedicineSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for Prescription CRUD operations"""
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Prescription.objects.all().select_related('patient', 'doctor', 'appointment')
        elif user.role == 'doctor':
            return Prescription.objects.filter(doctor=user).select_related('patient', 'doctor', 'appointment')
        elif user.role == 'patient':
            return Prescription.objects.filter(patient=user).select_related('patient', 'doctor', 'appointment')
        return Prescription.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PrescriptionCreateSerializer
        return PrescriptionSerializer
    
    def create(self, request, *args, **kwargs):
        # Only doctors can create prescriptions
        if request.user.role not in ['doctor', 'admin']:
            return Response(
                {'error': 'Only doctors can create prescriptions'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active prescriptions"""
        prescriptions = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(prescriptions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a prescription"""
        prescription = self.get_object()
        prescription.is_active = False
        prescription.save()
        return Response(PrescriptionSerializer(prescription).data)


# Django Views for HTML Pages
def prescriptions_page(request):
    """Render prescriptions page"""
    return render(request, 'prescriptions/prescriptions.html')


def prescription_detail_page(request, prescription_id):
    """Render prescription detail page"""
    return render(request, 'prescriptions/prescription_detail.html', {'prescription_id': prescription_id})
