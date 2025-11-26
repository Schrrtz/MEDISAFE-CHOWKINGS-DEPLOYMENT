# 📦 MediSafe+ Project Transfer Guide
## Complete Setup Instructions for Clean Device Installation

---

## 📋 TABLE OF CONTENTS
1. [Project Overview](#project-overview)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Checklist](#pre-installation-checklist)
4. [Installation Steps](#installation-steps)
5. [Database Setup](#database-setup)
6. [Configuration & Environment Variables](#configuration--environment-variables)
7. [Running the Project](#running-the-project)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 PROJECT OVERVIEW

### **Project Name:** MediSafe+
**Type:** Django-based Healthcare Management System  
**Database:** PostgreSQL (Supabase Cloud)  
**Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)  
**Version:** Django 5.2.6  
**Python Version:** 3.9+  

### **What the Project Does:**
MediSafe+ is a comprehensive healthcare management platform with:
- Patient profile management
- Lab results viewing and downloads
- Service booking system
- Doctor consultations
- Medical history tracking
- Health tools (BMI calculator, etc.)
- Admin dashboard for staff
- Notification system
- Prescription management

### **Key Features:**
✅ User authentication (Patient, Doctor, Admin, Nurse, Lab Tech roles)  
✅ Lab results management with file downloads  
✅ Service/appointment booking system  
✅ Real-time notifications  
✅ Multi-role authorization  
✅ Responsive design  
✅ Media management (photos, documents, prescriptions)  

---

## 💻 SYSTEM REQUIREMENTS

### **Minimum Requirements:**
- **OS:** Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python:** 3.9 or higher (3.11+ recommended)
- **RAM:** 4GB (8GB recommended)
- **Disk Space:** 500MB minimum
- **Internet:** Required (cloud database connection)

### **Required Software to Install:**
1. **Python 3.9+** - https://www.python.org/downloads/
2. **Git** - https://git-scm.com/downloads (optional, for version control)
3. **PostgreSQL Client** - https://www.postgresql.org/download/ (optional, for direct DB access)

---

## ✅ PRE-INSTALLATION CHECKLIST

Before starting, ensure you have:

- [ ] Python 3.9+ installed and in PATH
- [ ] Administrator access to your machine
- [ ] Internet connection (stable)
- [ ] **Supabase Account** created (for database access)
- [ ] **Database credentials** from Supabase:
  - Host
  - Database name
  - Username
  - Password
  - Port (usually 5432)
- [ ] Approximately 500MB free disk space
- [ ] Text editor or IDE (VS Code recommended)

**⚠️ IMPORTANT DATABASE CREDENTIALS:**
```
Current Production Database: Supabase (AWS - Southeast Asia)
- Host: aws-1-ap-southeast-1.pooler.supabase.com
- Port: 5432
- SSL Mode: Required
```

---

## 🚀 INSTALLATION STEPS

### **Step 1: Create Project Directory**

```powershell
# Windows PowerShell
mkdir C:\MediSafe-Projects
cd C:\MediSafe-Projects

# Or on macOS/Linux
mkdir ~/MediSafe-Projects
cd ~/MediSafe-Projects
```

### **Step 2: Clone/Copy Project Files**

Option A - Copy existing project:
```powershell
# Copy the PBL folder to your projects directory
Copy-Item "path\to\source\PBL" -Destination "C:\MediSafe-Projects\PBL" -Recurse
cd C:\MediSafe-Projects\PBL
```

Option B - If using Git:
```powershell
git clone <repository-url>
cd PBL
```

### **Step 3: Create Python Virtual Environment**

```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Output should show:** `(venv)` prefix in terminal

### **Step 4: Install All Python Dependencies**

```powershell
# Upgrade pip first (IMPORTANT!)
python -m pip install --upgrade pip

# Install all required packages
pip install Django==5.2.6
pip install psycopg2-binary==2.9.10
pip install psycopg2==2.9.10
pip install pillow==11.3.0
pip install python-dotenv==1.1.1
pip install requests==2.32.3
pip install supabase==2.21.1
pip install cryptography==46.0.2
pip install mysql-connector-python==9.3.0
pip install sqlparse==0.5.3
pip install asgiref==3.9.1
pip install httpx==0.28.1
```

**Or install all at once from requirements file (if available):**
```powershell
pip install -r requirements.txt
```

### **Step 5: Create Environment Configuration File**

Create a `.env` file in the `PBL` directory (same level as `manage.py`):

```bash
# Django Configuration
DJANGO_SECRET_KEY=django-insecure-^_^z+g@c_wo-@$zq%wx4e^#9l2$)!=^rhv6=jqq_32ele0b107
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,testserver

# Database Configuration (Supabase PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.YOUR_SUPABASE_USER
DB_PASSWORD=YOUR_SUPABASE_PASSWORD
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=5432
DB_SSLMODE=require
DB_CONN_MAX_AGE=0

# Local Alternative (SQLite - for testing without database)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

---

## 🗄️ DATABASE SETUP

### **Important: Database Connection Options**

#### **Option A: Use Existing Cloud Database (Supabase)**

1. Contact the MediSafe+ admin for Supabase credentials
2. Add credentials to `.env` file (see Step 5 above)
3. Skip to "Running Migrations" section

#### **Option B: Set Up New Supabase Project**

1. Go to https://supabase.com and create account
2. Create new project (region: Southeast Asia recommended)
3. Get connection strings from Project Settings → Database
4. Add to `.env` file

#### **Option C: Use Local SQLite (Development Only)**

For development/testing without external database:

```bash
# In .env file:
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### **Running Database Migrations**

```powershell
cd C:\MediSafe-Projects\PBL

# Apply all migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to create admin account
```

### **Verify Database Connection**

```powershell
# Test Django shell connection
python manage.py shell
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute('SELECT 1')
>>> print("Database connected!")
>>> exit()
```

---

## ⚙️ CONFIGURATION & ENVIRONMENT VARIABLES

### **Complete .env Template**

```env
# ============================================
# DJANGO SETTINGS
# ============================================
DJANGO_SECRET_KEY=django-insecure-your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# ============================================
# DATABASE - PostgreSQL (Supabase)
# ============================================
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.user_id
DB_PASSWORD=your_secure_password
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=5432
DB_SSLMODE=require
DB_CONN_MAX_AGE=0

# ============================================
# SECURITY (Update for Production)
# ============================================
SESSION_COOKIE_SECURE=False          # Set to True in production
CSRF_COOKIE_SECURE=False             # Set to True in production
SESSION_COOKIE_HTTPONLY=True
SECURE_SSL_REDIRECT=False            # Set to True in production

# ============================================
# SESSION CONFIGURATION
# ============================================
SESSION_COOKIE_AGE=86400             # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE=False
SESSION_SAVE_EVERY_REQUEST=True
```

### **Key Configuration Files**

| File | Location | Purpose |
|------|----------|---------|
| `settings.py` | `PBL/MEDISAFE_PBL/settings.py` | Django configuration |
| `urls.py` | `PBL/MEDISAFE_PBL/urls.py` | URL routing |
| `manage.py` | `PBL/manage.py` | Management commands |
| `.env` | `PBL/.env` | Environment variables |
| `db.sqlite3` | `PBL/db.sqlite3` | Local database (if using SQLite) |

---

## 🏃 RUNNING THE PROJECT

### **Start Development Server**

```powershell
# Make sure virtual environment is activated
# Navigate to PBL directory
cd C:\MediSafe-Projects\PBL

# Run development server
python manage.py runserver

# Output should show:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C
```

### **Access the Application**

1. Open web browser
2. Navigate to: `http://127.0.0.1:8000`
3. You should see the MediSafe+ homepage

### **Access Admin Panel**

1. Navigate to: `http://127.0.0.1:8000/admin`
2. Login with superuser credentials created during migration
3. Manage users, view database tables

---

## 📂 PROJECT STRUCTURE

```
PBL/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database (if used)
│
├── MEDISAFE_PBL/            # Main Django project config
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI config for deployment
│   ├── asgi.py              # ASGI config for deployment
│   └── __init__.py
│
├── myapp/                   # Main application
│   ├── models.py            # Database models
│   ├── admin.py             # Admin panel configuration
│   ├── views.py             # View logic
│   ├── urls.py              # App URLs
│   ├── tests.py             # Unit tests
│   │
│   ├── features/            # Feature modules
│   │   ├── auth/            # Authentication
│   │   ├── dashboard/       # User dashboard
│   │   ├── medical/         # Lab results (lab_results.html)
│   │   ├── profiles/        # User profiles
│   │   ├── consultations/   # Doctor consultations
│   │   ├── doctors/         # Doctor management
│   │   ├── admin/           # Admin panel
│   │   ├── patients/        # Patient management
│   │   ├── healthtools/     # Health calculators
│   │   ├── conditions/      # Medical conditions
│   │   └── home/            # Homepage
│   │
│   ├── static/              # CSS, JS, Images
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── templates/           # HTML templates
│   │   └── base.html        # Base template
│   │
│   ├── media/               # User uploaded media
│   │   ├── profile_photos/
│   │   ├── LAB PICTURES/
│   │   ├── notifications/
│   │   ├── prescriptions/
│   │   └── cover_photos/
│   │
│   └── migrations/          # Database migrations
│
├── media/                   # Media root directory
├── templates/               # Root templates
├── static/                  # Root static files
│
├── venv/                    # Virtual environment
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── db.sqlite3              # SQLite database (optional)
```

---

## 🗂️ DATABASE MODELS OVERVIEW

### **Core Models**

#### **1. User Model**
- Fields: `user_id`, `username`, `email`, `password`, `role`, `status`, `date_joined`
- Roles: Admin, Doctor, Nurse, Lab Technician, Patient
- Extends Django's AbstractBaseUser

#### **2. UserProfile Model**
- Linked to User (OneToOne)
- Fields: `first_name`, `last_name`, `birthday`, `sex`, `contact_number`, `photo_url`
- Stores additional user information

#### **3. Doctor Model**
- Fields: `specialization`, `license_number`, `years_of_experience`, `availability`
- Linked to User (OneToOne)

#### **4. Appointment Model**
- Fields: `appointment_number`, `patient`, `doctor`, `date`, `time`, `duration_minutes`, `status`
- Status options: Pending, Confirmed, Completed, Cancelled

#### **5. LabResult Model**
- Fields: `lab_type`, `upload_date`, `file_type`, `file`, `uploaded_by`, `test_name`
- Stores lab test results and uploaded files

#### **6. Prescription Model**
- Fields: `prescription_date`, `medication`, `dosage`, `frequency`, `duration`, `notes`

#### **7. Notification Model**
- Fields: `recipient`, `message`, `type`, `is_read`, `created_at`
- Tracks user notifications

---

## 🔧 COMMON COMMANDS

### **Django Management Commands**

```powershell
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Create test data
python manage.py shell
>>> from myapp.models import User
>>> User.objects.create_user(username='testuser', email='test@example.com', password='pass123', role='patient')

# Collect static files (for production)
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Access shell
python manage.py shell

# Check system health
python manage.py check

# Reset database (WARNING: deletes all data!)
python manage.py flush
```

---

## 🆘 TROUBLESHOOTING

### **Issue 1: "No module named 'django'"**
```powershell
# Solution: Install Django
pip install Django==5.2.6

# Or reinstall all dependencies
pip install -r requirements.txt
```

### **Issue 2: "Database connection refused"**
```powershell
# Check database credentials in .env
# Verify internet connection (cloud database requires it)
# Test connection:
python manage.py dbshell

# If using Supabase, verify:
# - Correct host URL
# - Port is 5432
# - SSL mode is 'require'
```

### **Issue 3: "Port 8000 already in use"**
```powershell
# Use different port
python manage.py runserver 8001

# Or find and kill process using port 8000
# Windows:
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### **Issue 4: "ModuleNotFoundError: No module named 'myapp'"**
```powershell
# Make sure you're in the PBL directory
cd C:\MediSafe-Projects\PBL

# Verify myapp is in INSTALLED_APPS in settings.py
# Run: python manage.py check
```

### **Issue 5: "psycopg2 installation failed"**
```powershell
# Install binary version instead
pip uninstall psycopg2
pip install psycopg2-binary==2.9.10
```

### **Issue 6: "Static files not loading"**
```powershell
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATICFILES_DIRS in settings.py
```

### **Issue 7: "Login not working"**
```powershell
# Ensure database has users
python manage.py shell
>>> from myapp.models import User
>>> User.objects.all()

# Create test user if needed:
>>> User.objects.create_user(username='admin', email='admin@test.com', password='admin123', role='admin')
```

---

## 📱 FEATURES & MODULES

### **Feature Modules**

| Module | URL Path | Description |
|--------|----------|-------------|
| **Home** | `/` | Landing page, homepage |
| **Auth** | `/auth/`, `/login/`, `/register/`, `/logout/` | Authentication |
| **Dashboard** | `/dashboard/` | User dashboard |
| **Medical** | `/lab-results/`, `/lab-services/` | Lab results management |
| **Profiles** | `/profile/`, `/profile/edit/` | User profiles |
| **Consultations** | `/appointments/`, `/consultations/` | Doctor appointments |
| **Doctors** | `/doctors/`, `/doctors/<id>/` | Doctor directory |
| **Patients** | `/patients/` | Patient records |
| **Health Tools** | `/health-tools/` | BMI calculator, etc. |
| **Admin** | `/admin-panel/` | Admin dashboard |
| **Conditions** | `/medical-conditions/` | Medical conditions database |

---

## 🚢 DEPLOYMENT NOTES

### **For Production Deployment:**

1. **Update .env settings:**
   ```bash
   DJANGO_DEBUG=False
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   SECURE_SSL_REDIRECT=True
   ```

2. **Use production database** (not SQLite)

3. **Collect static files:**
   ```powershell
   python manage.py collectstatic --noinput
   ```

4. **Use production WSGI server** (Gunicorn, uWSGI, etc.)

5. **Set up HTTPS/SSL certificate**

6. **Update ALLOWED_HOSTS** with production domain

---

## 📞 SUPPORT & RESOURCES

### **Useful Links**
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Supabase: https://supabase.com/docs
- Python: https://docs.python.org/3/

### **File Changes Made**
- `lab_results.html` - Enhanced UI with professional design
- Slideshow functionality for lab images
- Improved form validation and styling
- Enhanced table layouts with better scrolling

---

## ✅ VERIFICATION CHECKLIST

After installation, verify:

- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file created with database credentials
- [ ] Database migrations applied (`python manage.py migrate`)
- [ ] Development server runs without errors
- [ ] Can access `http://127.0.0.1:8000`
- [ ] Can access admin panel with superuser
- [ ] Database connection working
- [ ] Media files loading correctly
- [ ] Static files serving properly

---

## 📝 QUICK START COMMAND SUMMARY

```powershell
# Complete setup from scratch
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install Django==5.2.6 psycopg2-binary pillow python-dotenv requests supabase cryptography
# Create .env file with database credentials
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://127.0.0.1:8000
```

---

**Document Version:** 1.0  
**Last Updated:** November 26, 2025  
**Project:** MediSafe+ Healthcare Management System  
**Maintained By:** Development Team
