from django.contrib import admin
from .models import Prescription, PrescriptionMedicine


class PrescriptionMedicineInline(admin.TabularInline):
    model = PrescriptionMedicine
    extra = 1


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'appointment', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('patient__email', 'doctor__email', 'diagnosis')
    inlines = [PrescriptionMedicineInline]


@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medicine_name', 'dosage', 'frequency', 'duration')
    search_fields = ('medicine_name', 'prescription__patient__email')
