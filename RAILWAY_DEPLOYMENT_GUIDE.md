# 🚀 MEDISAFE+ Railway Deployment Guide

**Complete step-by-step guide to deploy MediSafe+ on Railway with PostgreSQL database**

---

## 📋 PROJECT ANALYSIS SUMMARY

### Technology Stack
- **Backend:** Django 5.2.6 (Python web framework)
- **Database:** PostgreSQL 
- **Python Version:** 3.9+ (3.11+ recommended)
- **App Type:** Web application with authentication & file uploads
- **Server:** WSGI (Gunicorn)

### Database Models (14 Core Tables)
1. **User** - Custom auth model (5 roles: admin, doctor, nurse, lab_tech, patient)
2. **UserProfile** - Extended user information
3. **Doctor** - Doctor specialization & details
4. **Patient** - Patient medical records
5. **Appointment** - Consultations (F2F & Tele)
6. **LabResult** - Lab test results with file uploads
7. **LiveAppointment** - Live consultation sessions
8. **Prescription** - Doctor prescriptions
9. **BookedService** - Service bookings
10. **Notification** - User notifications
11. **RolePermission** - Role access control

### Key Features
✅ Role-based authentication (5 roles)  
✅ File uploads (profile photos, lab results, prescriptions)  
✅ Media management (/media/ folder)  
✅ Static files (CSS, JS, Images)  
✅ 10 feature modules (auth, dashboard, medical, etc.)  
✅ Session-based authentication (24-hour timeout)  

### Current Configuration
- **Database:** PostgreSQL via Supabase (AWS Southeast Asia)
- **Media Storage:** Local file system (/media/ folder)
- **Static Files:** Collected in /staticfiles/ folder
- **DEBUG Mode:** Environment variable controlled
- **ALLOWED_HOSTS:** Environment variable controlled

---

## 🎯 WHAT'S NEEDED FOR RAILWAY DEPLOYMENT

### Prerequisites
1. ✅ **Railway Account** - Create at https://railway.app
2. ✅ **GitHub Account** - For version control
3. ✅ **Git Installation** - On your machine
4. ✅ **Project on GitHub** - Push your code there

### Railway Services Needed
1. **Django App Service** - Your application
2. **PostgreSQL Database** - For data storage
3. **File Storage** - For media uploads (Railway's persistent volume or S3)

### Configuration Files Needed
1. **Procfile** - Tells Railway how to run your app
2. **.env.production** - Production environment variables
3. **runtime.txt** - Python version specification
4. **Dockerfile** (Optional) - For custom deployment

### Code Changes Required
1. **Security Settings** - Set production flags
2. **Database Configuration** - Already environment-ready ✅
3. **Media File Handling** - Set up persistent storage
4. **Static Files** - Configure collection

---

## 📝 STEP-BY-STEP DEPLOYMENT PROCESS

### STEP 1: Prepare Your Local Project

#### 1.1 Create Required Configuration Files

**Create `Procfile` in project root:**
```
web: gunicorn MEDISAFE_PBL.wsgi:application
```

**Create `runtime.txt` in project root:**
```
python-3.11.9
```

**Create `.env.production` in project root (for reference only):**
```
# Production environment variables
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-generate-strong-random-string
DJANGO_ALLOWED_HOSTS=yourdomain.railway.app,www.yourdomain.com

# Database (will be provided by Railway PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=your-railway-db-password
DB_HOST=containers-us-west-XXX.railway.app
DB_PORT=5432
DB_SSLMODE=require

# File Storage
MEDIA_URL=/media/
MEDIA_ROOT=media/

# Session
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### 1.2 Create `.gitignore` (if not exists)

Add these entries to `.gitignore`:
```
*.pyc
__pycache__/
*.sqlite3
db.sqlite3
/venv
/env
.env
.env.local
.env.production
/staticfiles
/media
.DS_Store
node_modules/
```

#### 1.3 Update `requirements.txt`

Add gunicorn for production server:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

Your `requirements.txt` should include:
```
Django==5.2.6
gunicorn>=20.1.0
psycopg2-binary==2.9.10
python-dotenv==1.1.1
pillow==11.3.0
requests==2.32.3
# ... all other dependencies
```

#### 1.4 Update `settings.py` for Production

Modify `MEDISAFE_PBL/settings.py`:

**Find and update these sections:**

```python
# Line ~27: DEBUG setting
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes', 'on')

# Line ~29: ALLOWED_HOSTS for Railway
ALLOWED_HOSTS = [h.strip() for h in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')]

# Line ~199: Add security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Keep this FIRST
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of middleware
]

# Add after MIDDLEWARE (around line ~210):
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# Line ~230: Database - already environment-ready
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'railway'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': os.getenv('DB_SSLMODE', 'require'),
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}

# Add static files whitenoise (for serving CSS, JS without Django)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'myapp' / 'static',
    BASE_DIR / 'myapp' / 'features' / 'doctors',
]

# Media files configuration
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### STEP 2: Push Code to GitHub

#### 2.1 Initialize Git Repository (if not done)
```bash
cd "d:\DOWNLOADS\PBL - LATEST\PBL - fixed lab result - Copy\PBL"
git init
git add .
git commit -m "Initial commit for Railway deployment"
```

#### 2.2 Create GitHub Repository
1. Go to https://github.com/new
2. Create new repository (e.g., `medisafe-plus`)
3. Do NOT initialize with README
4. Copy the URL

#### 2.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/medisafe-plus.git
git branch -M main
git push -u origin main
```

### STEP 3: Set Up Railway Account

#### 3.1 Create Railway Account
1. Visit https://railway.app
2. Click "Start Free"
3. Sign up with GitHub (recommended)

#### 3.2 Create New Project
1. Click "New Project"
2. Click "Deploy from GitHub repo"
3. Select your `medisafe-plus` repository
4. Authorize Railway to access your GitHub

### STEP 4: Configure Railway Services

#### 4.1 Add PostgreSQL Database

**In Railway Dashboard:**
1. Click "Add Service" in your project
2. Select "Database" → "PostgreSQL"
3. PostgreSQL will be automatically added
4. Note the connection details provided

#### 4.2 Add Django Application

**In Railway Dashboard:**
1. Click "Add Service"
2. Select "GitHub Repo" 
3. Select your `medisafe-plus` repository
4. Railway auto-detects `Procfile` and runs your app

#### 4.3 Configure Environment Variables

**For Django App Service:**

Click on your Django service, go to "Variables" tab, add:

| Key | Value | Notes |
|-----|-------|-------|
| DJANGO_DEBUG | False | Production mode |
| DJANGO_SECRET_KEY | Generate a strong random key | Use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| DJANGO_ALLOWED_HOSTS | your-app.railway.app | Update after deployment |
| DB_ENGINE | django.db.backends.postgresql | Database engine |
| DB_NAME | railway | Default Railway DB name |
| DB_USER | postgres | Default user |
| DB_PASSWORD | Copy from PostgreSQL service variables | |
| DB_HOST | Copy from PostgreSQL service variables | |
| DB_PORT | 5432 | Standard PostgreSQL port |
| DB_SSLMODE | require | Secure connection |
| PYTHONUNBUFFERED | 1 | Python output buffering |

**How to get PostgreSQL variables:**
1. Click on the PostgreSQL service in Railway
2. Go to "Variables" tab
3. Look for `DATABASE_URL` or individual vars:
   - `PGHOST` = DB_HOST
   - `PGUSER` = DB_USER
   - `PGPASSWORD` = DB_PASSWORD
   - `PGPORT` = DB_PORT
   - `PGDATABASE` = DB_NAME

### STEP 5: Database Migrations & Setup

#### 5.1 Connect to Railway PostgreSQL

After deployment starts, you need to run migrations. In Railway:

**Option A: Run via Railway CLI (Recommended)**

```bash
# Install Railway CLI
npm install -g @railway/cli
# or use: curl -fsSL https://railway.app/install.sh | bash

# Login to Railway
railway login

# Navigate to your project directory
cd d:\DOWNLOADS\PBL - LATEST\PBL - fixed lab result - Copy\PBL

# Link to your Railway project
railway link

# Run migrations on production database
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Collect static files
railway run python manage.py collectstatic --noinput
```

**Option B: SSH into Railway Container**

In Railway Dashboard:
1. Click your Django service
2. Go to "Deployments" tab
3. Find latest deployment
4. Click "Deploy Logs" → "SSH" button
5. Run commands in the container:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### 5.2 Verify Database Connection

Run in Railway container:
```bash
python manage.py shell
```

Then in Python shell:
```python
from django.db import connection
connection.ensure_connection()
print("Database connected!")

# List all tables
from django.core.management import call_command
call_command('migrate', '--list')
```

### STEP 6: Handle Media & Static Files

#### 6.1 Static Files Configuration

**Already configured in settings.py:**
```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Railway collects static automatically.**

Run before deployment:
```bash
python manage.py collectstatic --noinput
```

#### 6.2 Media Files (Important!)

Railway has **ephemeral file storage** - files deleted on redeploy!

**Solution 1: Use Railway Persistent Volume (Free)**

In Railway Dashboard:
1. Click Django service
2. Go to "Settings" tab
3. Add Volume:
   - Mount Path: `/app/media`
   - Size: As needed

**Solution 2: Use AWS S3 (Production-Ready)**

Install package:
```bash
pip install django-storages boto3
```

Update `settings.py`:
```python
# At top of settings.py
if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "ACCESS_KEY_ID": os.getenv('AWS_ACCESS_KEY_ID'),
                "SECRET_ACCESS_KEY": os.getenv('AWS_SECRET_ACCESS_KEY'),
                "STORAGE_BUCKET_NAME": os.getenv('AWS_STORAGE_BUCKET_NAME'),
                "S3_REGION_NAME": 'us-east-1',
                "S3_CUSTOM_DOMAIN": f"{os.getenv('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com",
            }
        }
    }
    MEDIA_URL = f"https://{os.getenv('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/media/"
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Update requirements.txt with:
# django-storages==1.14.2
# boto3==1.34.46
```

Add S3 variables in Railway:
```
AWS_ACCESS_KEY_ID=your-s3-key
AWS_SECRET_ACCESS_KEY=your-s3-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### STEP 7: First Deployment

#### 7.1 Deploy Application

In Railway Dashboard:
1. Click your Django service
2. Go to "Deployments" tab
3. Click "Deploy" or just push to main branch
4. Railway auto-deploys on push to GitHub

#### 7.2 Monitor Deployment

1. Watch deployment logs in Railway Dashboard
2. Check for errors in "Deploy Logs"
3. Verify service is "Running" (green status)

#### 7.3 Access Your Application

**Find your URL:**
1. Click Django service
2. Copy the domain (e.g., `medisafe-xxxxx.railway.app`)
3. Visit: `https://medisafe-xxxxx.railway.app`

### STEP 8: Post-Deployment Configuration

#### 8.1 Update ALLOWED_HOSTS

After getting your Railway domain:

1. In Railway Dashboard → Django service → Variables
2. Update `DJANGO_ALLOWED_HOSTS`:
   ```
   medisafe-xxxxx.railway.app,www.medisafe-xxxxx.railway.app
   ```
3. Railway auto-redeploys

#### 8.2 Create First Admin User

SSH into container (see STEP 5.2):
```bash
python manage.py createsuperuser
# Follow prompts
```

#### 8.3 Access Admin Panel

Visit: `https://your-railway-domain/admin`
- Login with superuser credentials
- Verify all models in admin

#### 8.4 Test Key Features

1. **Authentication:**
   - Test login/logout
   - Create test users with different roles

2. **File Uploads:**
   - Upload profile photo
   - Upload lab results
   - Verify files save correctly

3. **Database:**
   - Check appointments appear
   - Verify notifications send
   - Test notifications read status

#### 8.5 Enable Production Monitoring

In Railway Dashboard:
1. Click your project
2. Go to "Settings"
3. Enable monitoring
4. Check metrics dashboard

---

## 🔧 TROUBLESHOOTING COMMON ISSUES

### Issue 1: Database Connection Failed

**Error:** `could not translate host name "localhost" to address`

**Solution:**
1. Check DB_HOST variable in Railway (should be containers-us-west-XXX.railway.app)
2. Verify DB_PASSWORD matches PostgreSQL service
3. Ensure DB_SSLMODE = require
4. Test locally with same connection string

**Debug:**
```bash
railway run python manage.py dbshell
```

### Issue 2: Static Files Not Loading (404)

**Error:** CSS/JS returns 404

**Solution:**
```bash
# Run in Railway container
python manage.py collectstatic --noinput --clear

# Then redeploy
```

### Issue 3: Media Files Disappear After Redeploy

**Solution:**
- Use persistent volume (see STEP 6.2)
- Or switch to S3 storage

### Issue 4: Secret Key Not Set

**Error:** `DJANGO_SECRET_KEY` environment variable error

**Solution:**
1. Generate strong key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Add to Railway Variables
3. Redeploy

### Issue 5: ALLOWED_HOSTS Mismatch

**Error:** `Invalid HTTP_HOST header`

**Solution:**
1. Update `DJANGO_ALLOWED_HOSTS` with your Railway domain
2. Redeploy

### Issue 6: Permission Denied on Media Upload

**Error:** `Permission denied` when uploading files

**Solution:**
- If using persistent volume, ensure media folder has correct permissions
- Or use S3 storage (recommended)

### Issue 7: Out of Memory (503 Error)

**Error:** Application keeps crashing with memory errors

**Solution:**
1. In Railway → Service Settings → increase Memory
2. Or optimize database queries
3. Use database connection pooling

---

## 📊 VERIFICATION CHECKLIST

After deployment, verify:

- [ ] Django app is deployed and running (green status in Railway)
- [ ] PostgreSQL database is created and connected
- [ ] Admin panel is accessible at `/admin`
- [ ] Can login with superuser account
- [ ] Static files load (CSS, JavaScript)
- [ ] Media uploads work
- [ ] All database models appear in admin
- [ ] Can create users with different roles
- [ ] Appointments can be created
- [ ] Lab results can be uploaded
- [ ] Notifications system works
- [ ] Email configuration working (if applicable)
- [ ] Domain shows in browser without errors
- [ ] HTTPS connection is secure

---

## 🔐 SECURITY BEST PRACTICES

✅ **Before going public, ensure:**

1. **DEBUG = False** in production
2. **Strong DJANGO_SECRET_KEY** (40+ random characters)
3. **HTTPS enabled** (Railway auto-provides SSL)
4. **CSRF_COOKIE_SECURE = True**
5. **SESSION_COOKIE_SECURE = True**
6. **ALLOWED_HOSTS set correctly**
7. **Separate production database** (not shared with development)
8. **Strong database password** (30+ characters)
9. **Disable DEBUG logging** in production
10. **Regular database backups** enabled in Railway

---

## 📱 CUSTOM DOMAIN SETUP (Optional)

### Add Custom Domain to Railway

1. In Railway → Project Settings
2. Go to "Domains" section
3. Click "Add Custom Domain"
4. Enter your domain (e.g., medisafe.com)
5. Railway provides DNS records to add
6. Update DNS with your registrar
7. Wait 24-48 hours for DNS propagation

### Example DNS Records:
```
CNAME: your-subdomain → medisafe-xxxxx.railway.app
```

---

## 📞 GETTING HELP

### Railway Documentation
- https://docs.railway.app
- https://docs.railway.app/deploy/deployments
- https://docs.railway.app/databases/postgresql

### Django Documentation
- https://docs.djangoproject.com/en/5.2/
- https://docs.djangoproject.com/en/5.2/howto/deployment/
- https://docs.djangoproject.com/en/5.2/ref/settings/

### Common Commands

```bash
# Local testing before Railway
python manage.py runserver

# Run migrations locally
python manage.py migrate

# Create superuser locally
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test settings
python manage.py check

# Access Railway shell
railway shell

# View logs
railway logs

# Execute command in Railway
railway run python manage.py [command]
```

---

## ✅ DEPLOYMENT SUMMARY

| Step | Task | Status |
|------|------|--------|
| 1 | Create configuration files (Procfile, runtime.txt) | Ready |
| 2 | Add gunicorn to requirements.txt | Ready |
| 3 | Update settings.py for production | Ready |
| 4 | Push code to GitHub | Ready |
| 5 | Create Railway account | You do this |
| 6 | Add PostgreSQL service | You do this |
| 7 | Add Django service | You do this |
| 8 | Configure environment variables | You do this |
| 9 | Run migrations in Railway | You do this |
| 10 | Access application & test | You do this |

**Estimated Time:** 30-45 minutes  
**Cost:** Free tier available ($5/month minimum after)  
**Support:** Railway support + Django community

---

## 🎯 NEXT STEPS

1. **Create Procfile** (provided above)
2. **Update requirements.txt** with gunicorn
3. **Modify settings.py** (follow instructions above)
4. **Push to GitHub**
5. **Create Railway account**
6. **Follow STEP 4-8** in this guide
7. **Test deployment**
8. **Share your live domain!**

---

**Last Updated:** November 26, 2025  
**Version:** 1.0  
**Status:** Ready for Deployment ✅

