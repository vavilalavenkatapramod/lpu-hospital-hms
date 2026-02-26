"""
Management command to seed initial data for HMS
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Doctor, Patient
from appointments.models import Appointment, AppointmentSlot
from prescriptions.models import Prescription, PrescriptionMedicine
from billing.models import Invoice, Payment
from django.utils import timezone
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create Admin User
        admin_user, created = User.objects.get_or_create(
            email='admin@hms.com',
            defaults={
                'username': 'admin',
                'first_name': 'System',
                'last_name': 'Admin',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.email}'))
        
        # Create Doctors
        doctors_data = [
            {'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith@hms.com',
             'specialization': 'Cardiology', 'qualification': 'MD, FACC', 'experience_years': 15,
             'license_number': 'DOC001', 'consultation_fee': 5000},
            {'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah.johnson@hms.com',
             'specialization': 'Neurology', 'qualification': 'MD, PhD', 'experience_years': 12,
             'license_number': 'DOC002', 'consultation_fee': 4500},
            {'first_name': 'Michael', 'last_name': 'Brown', 'email': 'michael.brown@hms.com',
             'specialization': 'Orthopedics', 'qualification': 'MS, MCH', 'experience_years': 10,
             'license_number': 'DOC003', 'consultation_fee': 4000},
            {'first_name': 'Emily', 'last_name': 'Davis', 'email': 'emily.davis@hms.com',
             'specialization': 'Pediatrics', 'qualification': 'MD, DNB', 'experience_years': 8,
             'license_number': 'DOC004', 'consultation_fee': 3500},
            {'first_name': 'Robert', 'last_name': 'Wilson', 'email': 'robert.wilson@hms.com',
             'specialization': 'Dermatology', 'qualification': 'MD, FAAD', 'experience_years': 11,
             'license_number': 'DOC005', 'consultation_fee': 3800},
        ]
        
        doctors = []
        for doc_data in doctors_data:
            user, created = User.objects.get_or_create(
                email=doc_data['email'],
                defaults={
                    'username': doc_data['email'].split('@')[0],
                    'first_name': doc_data['first_name'],
                    'last_name': doc_data['last_name'],
                    'role': 'doctor',
                    'is_verified': True
                }
            )
            if created:
                user.set_password('doctor123')
                user.save()
            
            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'specialization': doc_data['specialization'],
                    'qualification': doc_data['qualification'],
                    'experience_years': doc_data['experience_years'],
                    'license_number': doc_data['license_number'],
                    'consultation_fee': doc_data['consultation_fee'],
                    'is_available': True
                }
            )
            doctors.append(doctor)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created doctor: Dr. {user.get_full_name}'))
        
        # Create Patients
        patients_data = [
            {'first_name': 'James', 'last_name': 'Anderson', 'email': 'james.anderson@email.com',
             'blood_type': 'O+', 'phone': '9876543210'},
            {'first_name': 'Maria', 'last_name': 'Garcia', 'email': 'maria.garcia@email.com',
             'blood_type': 'A+', 'phone': '9876543211'},
            {'first_name': 'David', 'last_name': 'Lee', 'email': 'david.lee@email.com',
             'blood_type': 'B+', 'phone': '9876543212'},
            {'first_name': 'Jennifer', 'last_name': 'Martinez', 'email': 'jennifer.martinez@email.com',
             'blood_type': 'AB+', 'phone': '9876543213'},
            {'first_name': 'William', 'last_name': 'Taylor', 'email': 'william.taylor@email.com',
             'blood_type': 'O-', 'phone': '9876543214'},
            {'first_name': 'Lisa', 'last_name': 'Thomas', 'email': 'lisa.thomas@email.com',
             'blood_type': 'A-', 'phone': '9876543215'},
            {'first_name': 'Christopher', 'last_name': 'Harris', 'email': 'christopher.harris@email.com',
             'blood_type': 'B-', 'phone': '9876543216'},
            {'first_name': 'Amanda', 'last_name': 'Clark', 'email': 'amanda.clark@email.com',
             'blood_type': 'O+', 'phone': '9876543217'},
        ]
        
        patients = []
        for pat_data in patients_data:
            user, created = User.objects.get_or_create(
                email=pat_data['email'],
                defaults={
                    'username': pat_data['email'].split('@')[0],
                    'first_name': pat_data['first_name'],
                    'last_name': pat_data['last_name'],
                    'role': 'patient',
                    'phone': pat_data['phone'],
                    'is_verified': True
                }
            )
            if created:
                user.set_password('patient123')
                user.save()
            
            patient, created = Patient.objects.get_or_create(
                user=user,
                defaults={
                    'blood_type': pat_data['blood_type']
                }
            )
            patients.append(patient)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created patient: {user.get_full_name}'))
        
        # Create Appointments
        statuses = ['confirmed', 'pending', 'completed', 'cancelled']
        times = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
        for i, patient in enumerate(patients[:5]):
            doctor = doctors[i % len(doctors)]
            appointment_date = timezone.now() + timedelta(days=random.randint(-7, 14))
            status = random.choice(statuses)
            appointment_time = random.choice(times)
            
            appointment, created = Appointment.objects.get_or_create(
                patient=patient.user,
                doctor=doctor.user,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                defaults={
                    'status': status,
                    'reason': f'Regular checkup - {random.randint(1, 5)}th visit'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created appointment for {patient.user.get_full_name}'))
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.WARNING('Login credentials:'))
        self.stdout.write(self.style.WARNING('Admin: admin@hms.com / admin123'))
        self.stdout.write(self.style.WARNING('Doctor: john.smith@hms.com / doctor123'))
        self.stdout.write(self.style.WARNING('Patient: james.anderson@email.com / patient123'))
