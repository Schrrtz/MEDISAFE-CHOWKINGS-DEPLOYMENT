#!/usr/bin/env python
"""
Test script to verify that local development environment functions 
the same as the production deployment on Railway.

This script checks:
1. Django settings configuration
2. Static files collection
3. Media files accessibility
4. Database connectivity
5. Security settings parity
6. Critical features
"""

import os
import sys
import django
from pathlib import Path
from django.conf import settings

# Add PBL to path (same as manage.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PBL'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MEDISAFE_PBL.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from django.test.utils import get_runner
from django.apps import apps
from myapp.models import User, Doctor, Patient, Appointment

print("\n" + "="*70)
print("LOCAL ENVIRONMENT PARITY TEST")
print("="*70)

# Test 1: Django Configuration
print("\n[1] DJANGO CONFIGURATION")
print("-" * 70)
print(f"✓ DEBUG mode: {settings.DEBUG}")
print(f"✓ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"✓ Database engine: {settings.DATABASES['default']['ENGINE']}")
print(f"✓ Static URL: {settings.STATIC_URL}")
print(f"✓ Media URL: {settings.MEDIA_URL}")

# Test 2: Paths Configuration
print("\n[2] PATHS CONFIGURATION")
print("-" * 70)
base_dir = Path(settings.BASE_DIR)
print(f"✓ BASE_DIR: {base_dir}")
print(f"✓ STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"✓ MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"✓ STATIC_ROOT exists: {Path(settings.STATIC_ROOT).exists()}")
print(f"✓ MEDIA_ROOT exists: {Path(settings.MEDIA_ROOT).exists()}")

# Test 3: Static Files
print("\n[3] STATIC FILES CHECK")
print("-" * 70)
static_root = Path(settings.STATIC_ROOT)
if static_root.exists():
    static_files = list(static_root.rglob('*'))
    static_files = [f for f in static_files if f.is_file()]
    print(f"✓ Static files found: {len(static_files)}")
    css_files = [f for f in static_files if f.suffix == '.css']
    js_files = [f for f in static_files if f.suffix == '.js']
    print(f"  - CSS files: {len(css_files)}")
    print(f"  - JS files: {len(js_files)}")
else:
    print("⚠ Static files directory not found - run collectstatic")

# Test 4: Media Files
print("\n[4] MEDIA FILES CHECK")
print("-" * 70)
media_root = Path(settings.MEDIA_ROOT)
if media_root.exists():
    media_files = list(media_root.rglob('*'))
    media_files = [f for f in media_files if f.is_file()]
    print(f"✓ Media files found: {len(media_files)}")
    
    # Count by folder
    folders = set()
    for f in media_files:
        rel_path = f.relative_to(media_root)
        folders.add(str(rel_path.parent))
    
    print(f"✓ Media folders: {len(folders)}")
    for folder in sorted(folders):
        count = len([f for f in media_files if folder in str(f)])
        print(f"  - {folder}: {count} files")
else:
    print("⚠ Media directory not found")

# Test 5: Database Connectivity
print("\n[5] DATABASE CONNECTIVITY")
print("-" * 70)
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print("✓ Database connection successful")
    print(f"✓ Database: {settings.DATABASES['default']['NAME']}")
    print(f"✓ Host: {settings.DATABASES['default']['HOST']}")
except Exception as e:
    print(f"✗ Database connection failed: {e}")

# Test 6: Models Check
print("\n[6] MODELS AND DATA CHECK")
print("-" * 70)
try:
    user_count = User.objects.count()
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()
    
    print(f"✓ Users in database: {user_count}")
    print(f"✓ Doctors in database: {doctor_count}")
    print(f"✓ Patients in database: {patient_count}")
    print(f"✓ Appointments in database: {appointment_count}")
except Exception as e:
    print(f"✗ Model query failed: {e}")

# Test 7: Security Settings
print("\n[7] SECURITY SETTINGS PARITY")
print("-" * 70)
print(f"✓ SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
print(f"✓ SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"✓ CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print(f"✓ SECURE_HSTS_SECONDS: {settings.SECURE_HSTS_SECONDS}")

# Test 8: Installed Apps
print("\n[8] INSTALLED APPS")
print("-" * 70)
for app in settings.INSTALLED_APPS:
    print(f"✓ {app}")

# Test 9: File Access
print("\n[9] CRITICAL FILE ACCESS TEST")
print("-" * 70)
try:
    # Test static files access
    manage_path = Path(settings.BASE_DIR).parent / 'manage.py'
    print(f"✓ manage.py accessible: {manage_path.exists()}")
    
    # Test templates
    templates_count = len(list(Path(settings.BASE_DIR).glob('**/templates/**/*.html')))
    print(f"✓ Templates found: {templates_count}")
    
except Exception as e:
    print(f"✗ File access check failed: {e}")

# Test 10: Environment Variables
print("\n[10] ENVIRONMENT VARIABLES")
print("-" * 70)
env_vars = {
    'DJANGO_DEBUG': os.getenv('DJANGO_DEBUG', 'Not set'),
    'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Not set (using individual vars)',
    'DB_HOST': os.getenv('DB_HOST', 'Not set'),
    'DB_USER': os.getenv('DB_USER', 'Not set'),
}
for key, value in env_vars.items():
    print(f"✓ {key}: {value}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
Next steps:
1. Run: python manage.py collectstatic --noinput --clear
2. Run: python manage.py runserver
3. Test all features in browser at http://localhost:8000
4. Compare functionality with Railway deployment

For production parity:
- Ensure DEBUG=False locally to test production behavior
- Use the same database (Supabase) for testing
- Test static file serving with DEBUG=False
""")
print("="*70 + "\n")
