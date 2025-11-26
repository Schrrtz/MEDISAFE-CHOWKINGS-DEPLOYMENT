# Local Development Checklist

## ✅ Pre-Development Setup

- [ ] Virtual environment activated: `.\.venv\Scripts\Activate.ps1`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file exists in `PBL/` folder with database credentials
- [ ] Static files collected: `python manage.py collectstatic --noinput --clear`

## ✅ Before Starting Server

- [ ] Run system check: `python manage.py check`
- [ ] Run parity test: `python test_local_parity.py`
- [ ] Verify `STATIC_ROOT` exists: `D:\DOWNLOADS\PBL - LATEST\PBL - fixed lab result - Copy\staticfiles\`
- [ ] Verify `MEDIA_ROOT` exists: `PBL\media\`
- [ ] Database connectivity working (parity test confirms)

## ✅ Running Server

```powershell
# Navigate to project root
cd "d:\DOWNLOADS\PBL - LATEST\PBL - fixed lab result - Copy"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Collect static files
python manage.py collectstatic --noinput --clear

# Start development server
python manage.py runserver
```

## ✅ Testing Locally

### Test Checklist

#### 1. Static Files (CSS, JavaScript)
- [ ] Homepage loads with proper styling
- [ ] Doctor panel has correct layout
- [ ] Admin interface has proper CSS
- [ ] No 404 errors in browser console (F12)

#### 2. Media Files (Images, Uploads)
- [ ] Logo displays on homepage
- [ ] Doctor profile photos load
- [ ] Lab result images display
- [ ] User profile pictures show
- [ ] Prescriptions accessible

#### 3. Database & Features
- [ ] Login works
- [ ] Admin panel accessible
- [ ] User creation/editing works
- [ ] Appointments can be booked
- [ ] Lab results can be uploaded

#### 4. Key Pages
- [ ] Homepage: `http://localhost:8000`
- [ ] Admin: `http://localhost:8000/admin`
- [ ] Doctor Panel: Check styling and functionality
- [ ] Patient Dashboard: All widgets load
- [ ] Lab Results: Images display correctly

### Debugging Commands

```powershell
# Check for configuration issues
python manage.py check

# Test in Django shell
python manage.py shell
> from django.conf import settings
> print(settings.STATIC_ROOT)
> print(settings.MEDIA_ROOT)

# Verify static files
python manage.py findstatic --verbosity 2 app.js

# Reset database (careful!)
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

## ✅ Comparison: Local vs Production

When testing, verify same results for:

| Feature | Local | Production |
|---------|-------|-----------|
| Login/Auth | Works? | Works on Railway? |
| Static files | Loading? | Loading on Railway? |
| Media files | Displaying? | Displaying on Railway? |
| Doctor panel | Styled? | Styled on Railway? |
| Lab results | Images show? | Images show on Railway? |
| Forms | Submit? | Submit on Railway? |
| Database | Connected? | Connected to Supabase? |

## ✅ Deployment Process

```powershell
# 1. Test locally
python test_local_parity.py

# 2. Test all features
python manage.py runserver
# Visit http://localhost:8000 and test

# 3. Commit changes
git add -A
git commit -m "Your commit message"
git push origin main

# 4. Monitor Railway deployment
# Visit https://railway.app/dashboard
# Wait for build to complete (5-10 minutes)

# 5. Test production
# Visit https://medisafe-chowkings-deployment-production.up.railway.app
# Run same test checklist
```

## ✅ Troubleshooting Matrix

| Problem | Symptom | Solution |
|---------|---------|----------|
| Static files 404 | CSS/JS not loading | `python manage.py collectstatic --noinput --clear` |
| Media not showing | Images 404 | Verify `PBL/media/` exists with files |
| DB connection error | Can't connect | Check `.env` credentials, test with `python manage.py dbshell` |
| DEBUG error in prod | Site crashes with DEBUG=True | Set `DJANGO_DEBUG=False` in Railway environment |
| Template not found | 404 on page | Check template path in settings.py TEMPLATES |
| Permission denied | Can't upload | Check `PBL/media/` folder permissions |

## ✅ Critical Files to Verify

```
PBL/MEDISAFE_PBL/settings.py    ← Database, static, media paths
PBL/MEDISAFE_PBL/urls.py        ← URL routing and static serving
PBL/.env                        ← Database credentials
manage.py                       ← Root-level Django management
start.sh                        ← Railway deployment script
requirements.txt               ← Python dependencies
```

## ✅ Path References (Saved for Quick Lookup)

```
BASE_DIR = PBL/
STATIC_ROOT = Project root/staticfiles/
STATIC_DIRS = PBL/myapp/static/
MEDIA_ROOT = PBL/media/
```

## ✅ Quick Commands

```powershell
# Start fresh
python manage.py collectstatic --noinput --clear; python manage.py runserver

# Run all tests
python test_local_parity.py

# Create superuser
python manage.py createsuperuser

# Access admin
# Then visit http://localhost:8000/admin
```

## ✅ Expected Results After Setup

After completing setup, you should see:
- ✅ Static files: 148 files collected
- ✅ Media files: 45 files accessible
- ✅ Database: Connected to Supabase
- ✅ Users: 17 in database
- ✅ No warnings on `collectstatic`
- ✅ Server runs without errors

---

**Last Updated:** 2025-11-26  
**Ready for:** Local Testing & Production Deployment
