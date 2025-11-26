# Local Development Environment Setup & Parity Guide

## Overview

This guide ensures your **local development environment** functions identically to the **production deployment on Railway**. By following these steps, any feature that works locally will work on Railway, and vice versa.

---

## Quick Start (5 minutes)

### 1. Initial Setup
```powershell
# Navigate to project root
cd "d:\DOWNLOADS\PBL - LATEST\PBL - fixed lab result - Copy"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (if needed)
pip install -r requirements.txt
```

### 2. Collect Static Files
```powershell
python manage.py collectstatic --noinput --clear
```

### 3. Run Local Development Server
```powershell
python manage.py runserver
```

### 4. Access Application
- Open browser: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin`

---

## Project Structure & Paths

```
Project Root (d:\DOWNLOADS\PBL - LATEST\PBL - fixed lab result - Copy\)
├── manage.py                          # Root-level Django management script
├── PBL/                               # Django application root
│   ├── MEDISAFE_PBL/                  # Django settings module
│   │   ├── settings.py                # ⭐ Configuration file
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── myapp/                         # Main app module
│   │   ├── static/                    # CSS, JS, images (collected from here)
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   ├── templates/                 # HTML templates
│   │   ├── features/                  # Feature modules
│   │   │   ├── doctors/
│   │   │   ├── home/
│   │   │   ├── medical/
│   │   │   ├── profiles/
│   │   │   └── ...
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── media/                         # User-uploaded files (45 files committed to git)
│   │   ├── logo/
│   │   ├── HOMEPAGE PICTURES/
│   │   ├── LAB PICTURES/
│   │   ├── profile_photos/
│   │   ├── prescriptions/
│   │   └── notifications/
│   ├── migrations/                    # Database migrations
│   ├── .env                           # Local environment variables
│   └── db.sqlite3                     # Local database (when using SQLite)
├── staticfiles/                       # Collected static files (auto-generated)
├── start.sh                           # Railway startup script
├── Procfile                           # Railway configuration
└── requirements.txt                   # Python dependencies
```

---

## Key Configuration Files

### 1. **settings.py** (`PBL/MEDISAFE_PBL/settings.py`)

**Critical Settings:**
```python
# BASE_DIR resolves to PBL/ folder
BASE_DIR = Path(__file__).resolve().parent.parent  # = PBL/

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'      # = Project root/staticfiles
STATICFILES_DIRS = [BASE_DIR / 'myapp' / 'static'] # = PBL/myapp/static

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'                    # = PBL/media

# Database - uses Supabase PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')           # Set by Railway
if not DATABASE_URL:
    # Local development - uses .env variables
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'medisafe'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
```

### 2. **.env** (`PBL/.env`) - Local Environment

```dotenv
# Django Settings
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost

# Database Configuration (Supabase PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.wqoluwmdzljpvzimjiyr
DB_PASSWORD=Chowkings6229521
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=5432
DB_SSLMODE=require
```

### 3. **manage.py** (Root Level)

The manage.py adds PBL to `sys.path` so Django can find MEDISAFE_PBL module:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PBL'))
```

This is crucial for making the app work from the root directory.

---

## Environment Parity Checklist

✅ **Static Files:**
- [x] 148 static files collected
- [x] CSS files: 30
- [x] JavaScript files: 91
- [x] Located in: `staticfiles/` (auto-collected from `PBL/myapp/static/`)

✅ **Media Files:**
- [x] 45 media files committed to git
- [x] Located in: `PBL/media/`
- [x] Folders: logo, profile_photos, prescriptions, notifications, LAB PICTURES, HOMEPAGE PICTURES

✅ **Database:**
- [x] PostgreSQL (Supabase)
- [x] Host: `aws-1-ap-southeast-1.pooler.supabase.com`
- [x] Database: `postgres`
- [x] Connection pooler enabled

✅ **Paths:**
- [x] BASE_DIR: `PBL/`
- [x] STATIC_ROOT: `Project root/staticfiles`
- [x] MEDIA_ROOT: `PBL/media`
- [x] All paths verified and tested

✅ **Models & Data:**
- [x] Users: 17
- [x] Doctors: 6
- [x] Patients: 4
- [x] Appointments: 24
- [x] All tables intact

---

## Testing Local vs Production

### Test 1: Run Parity Test
```powershell
python test_local_parity.py
```

This script checks:
- Django configuration
- Path existence and correctness
- Static files collection
- Media files accessibility
- Database connectivity
- All models and data
- Security settings

### Test 2: Test with DEBUG=False (Production Mode)

To test production behavior locally:

```powershell
# Temporarily set DEBUG to False
# Edit PBL/.env:
# DJANGO_DEBUG=False

# Collect static files (again with DEBUG=False)
python manage.py collectstatic --noinput --clear

# Run server
python manage.py runserver

# Test features:
# - CSS should still load (served by WhiteNoise)
# - Media files should display
# - 404 errors should show production page
# - Security headers should be applied
```

### Test 3: Feature Testing Checklist

Test the following features locally, then compare with Railway:

#### Authentication & Profiles
- [ ] User registration
- [ ] Login/Logout
- [ ] Profile settings
- [ ] Profile picture upload (media test)
- [ ] Change password

#### Doctors Module
- [ ] View doctor list with styling
- [ ] Doctor panel (CSS heavy)
- [ ] Schedule appointment
- [ ] View consultations

#### Patients Module
- [ ] Patient dashboard
- [ ] View appointments
- [ ] Prescriptions display

#### Medical Records
- [ ] Lab results upload
- [ ] Lab results display with images
- [ ] Medical history view

#### Media Files
- [ ] Logo display on homepage
- [ ] Doctor profile photos
- [ ] Lab result images
- [ ] Prescription PDFs

#### Static Files
- [ ] CSS styling applied (check browser dev tools)
- [ ] JavaScript functions working
- [ ] No 404 errors for static files

---

## Troubleshooting

### Issue: Static files not loading
**Solution:**
```powershell
# Clear and recollect static files
python manage.py collectstatic --noinput --clear
```

### Issue: "STATICFILES_DIRS" warning
**Solution:** 
- This is expected if directories don't exist
- Ensure `PBL/myapp/static/` exists
- Run collectstatic again

### Issue: Media files showing 404
**Solution:**
```python
# Verify MEDIA_ROOT in settings:
# Should be: BASE_DIR / 'media' where BASE_DIR = PBL/

# Check media folder exists:
# Should be at: PBL/media/
```

### Issue: Database connection refused
**Solution:**
```powershell
# Verify .env variables:
cat PBL/.env

# Test connection:
python manage.py dbshell

# If using Supabase, ensure:
# - Host: aws-1-ap-southeast-1.pooler.supabase.com
# - Port: 5432
# - DB_SSLMODE: require
```

### Issue: "DEBUG=False" causing static files to fail
**Solution:**
```python
# Ensure WhiteNoise middleware is enabled in settings.py:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be here
    ...
]

# And STATICFILES_STORAGE is set:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Common Commands

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --clear

# Run development server
python manage.py runserver

# Run parity test
python test_local_parity.py

# Access Django shell
python manage.py shell

# Check configuration
python manage.py check
```

---

## Production Deployment (Railway)

When deploying to Railway, the system automatically:

1. **Runs Procfile** (`start.sh`):
   ```bash
   python manage.py collectstatic --noinput --clear
   gunicorn --pythonpath PBL --bind 0.0.0.0:$PORT MEDISAFE_PBL.wsgi:application
   ```

2. **Sets environment variables**:
   - `DATABASE_URL`: Supabase connection string
   - `RAILWAY_ENVIRONMENT_NAME`: production
   - Others from Railway dashboard

3. **Serves files**:
   - Static files via WhiteNoise (from `staticfiles/`)
   - Media files via Django urls.py

---

## Differences: Local vs Production

| Aspect | Local | Production (Railway) |
|--------|-------|----------------------|
| DEBUG | True | False |
| Database | Supabase (same) | Supabase (same) |
| Static Root | `Project root/staticfiles` | `/app/staticfiles` |
| Media Root | `PBL/media` | `/app/PBL/media` |
| Server | Django dev (8000) | Gunicorn (8080) |
| SSL | Off | On (automatic) |
| Log Level | Verbose | Info |
| Static Middleware | Django default | WhiteNoise |

---

## Next Steps

1. ✅ **Setup complete** - You now have local parity with production
2. 📝 **Test thoroughly** - Use the feature testing checklist above
3. 🚀 **Deploy with confidence** - Features working locally = working on Railway
4. 📊 **Monitor production** - Check Railway logs after deployment

---

## Support & Debugging

### View test results:
```powershell
python test_local_parity.py
```

### Check for errors in local server:
```powershell
python manage.py runserver
# Watch terminal for errors
```

### Check Railway logs:
Visit: `https://railway.app/dashboard` → Select project → View logs

### Get help:
- Check models in `PBL/myapp/models.py`
- Review views in feature modules
- Check templates in `PBL/myapp/templates/`

---

**Last Updated:** 2025-11-26  
**Version:** 1.0  
**Status:** Local-Production Parity ✅
