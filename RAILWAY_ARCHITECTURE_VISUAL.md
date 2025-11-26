# 🏗️ RAILWAY DEPLOYMENT ARCHITECTURE & FLOW GUIDE

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USERS (Internet)                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
         ┌─────────────────────────────────────┐
         │  RAILWAY DOMAIN (yourdomain.railway.app) │
         │  - Auto SSL/HTTPS                  │
         │  - Load Balancer                   │
         │  - CDN Support                     │
         └──────────────┬──────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌──────────────────────┐       ┌──────────────────────┐
│  DJANGO APP SERVICE  │       │  STATIC FILES (CSS/) │
│  ├─ Gunicorn Server  │       │  - Whitenoise        │
│  ├─ Python 3.11.9    │       │  - Compressed        │
│  ├─ Django 5.2.6     │       │  - Cached            │
│  ├─ 8 Workers        │       └──────────────────────┘
│  └─ Port 8000        │
└──────────────┬───────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
┌─────────────────────────────┐    ┌──────────────────┐
│  POSTGRESQL DATABASE        │    │  PERSISTENT VOL  │
│  ├─ 14 Tables              │    │  /app/media      │
│  ├─ Users (custom)         │    │  - Profile pics  │
│  ├─ Appointments           │    │  - Lab results   │
│  ├─ Lab Results            │    │  - Prescriptions │
│  ├─ Prescriptions          │    └──────────────────┘
│  ├─ Notifications          │
│  └─ Backups enabled        │
└─────────────────────────────┘
```

## Deployment Flow (Step by Step)

```
START
  │
  ├─► 1. LOCAL PREPARATION
  │   ├─ Create Procfile ✓
  │   ├─ Create runtime.txt ✓
  │   ├─ Update requirements.txt ✓
  │   ├─ Update settings.py ✓
  │   └─ Create .env.production
  │
  ├─► 2. PUSH TO GITHUB
  │   ├─ git add . 
  │   ├─ git commit
  │   ├─ git push origin main
  │   └─ Code on GitHub
  │
  ├─► 3. CREATE RAILWAY ACCOUNT
  │   ├─ Sign up at railway.app
  │   ├─ Create new project
  │   ├─ Connect GitHub repo
  │   └─ Authorize Railway
  │
  ├─► 4. ADD SERVICES
  │   ├─ Add PostgreSQL database
  │   ├─ Add Django app service
  │   └─ Railway detects Procfile
  │
  ├─► 5. SET ENVIRONMENT VARIABLES
  │   ├─ DJANGO_DEBUG=False
  │   ├─ DJANGO_SECRET_KEY=[key]
  │   ├─ DB_* [from PostgreSQL]
  │   └─ Security flags
  │
  ├─► 6. DEPLOYMENT STARTS
  │   ├─ Railway pulls from GitHub
  │   ├─ Installs requirements.txt
  │   ├─ Builds application
  │   ├─ Starts Gunicorn server
  │   └─ App goes live
  │
  ├─► 7. RUN MIGRATIONS
  │   ├─ SSH into container
  │   ├─ python manage.py migrate
  │   ├─ python manage.py createsuperuser
  │   ├─ python manage.py collectstatic
  │   └─ Database ready
  │
  ├─► 8. VERIFICATION
  │   ├─ Visit domain
  │   ├─ Login to admin
  │   ├─ Test features
  │   ├─ Check logs
  │   └─ Go live!
  │
  END - APP LIVE! 🚀
```

## File Upload & Storage Flow

```
USER UPLOADS FILE
        │
        ▼
┌─────────────────────┐
│  DJANGO VIEW        │
│  - Validates file   │
│  - Checks size      │
│  - Virus scan (opt) │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────────────────────────┐    ┌─────────────────┐
│  PERSISTENT VOLUME (Local) │    │  AWS S3 (Cloud) │
│  /app/media/               │    │  s3://bucket/   │
│  - Fast access             │    │  - Scalable     │
│  - Free with Railway       │    │  - Recommended  │
│  - Limited size            │    │  - ~$1/month    │
└────────────────────────────┘    └─────────────────┘
```

## Database Connection Flow

```
APPLICATION REQUEST
        │
        ▼
┌──────────────────────────┐
│  Django ORM              │
│  - Builds query          │
│  - Validates data        │
│  - Handles transactions  │
└──────────────┬───────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
    ┌─────────────────────────┐
    │  Connection Pooling     │
    │  - Max 600 connections  │
    │  - 10 minute timeout    │
    │  - SSL/TLS encrypted    │
    └──────────────┬──────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │  RAILWAY POSTGRESQL    │
        │  - Managed database    │
        │  - Automatic backups   │
        │  - High availability   │
        └────────────────────────┘
```

## Authentication Flow

```
USER VISITS WEBSITE
        │
        ▼
┌────────────────────────┐
│  NOT AUTHENTICATED     │
│  → Redirect to login   │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│  ENTER CREDENTIALS     │
│  Username + Password   │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────────────┐
│  DJANGO AUTHENTICATION BACKEND  │
│  - Query User table             │
│  - Check password hash          │
│  - Validate role                │
└────────────┬───────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
  SUCCESS      FAILED
      │             │
      ▼             ▼
┌──────────────┐  ┌─────────────────┐
│ CREATE SESS. │  │ Show error      │
│ Store in DB  │  │ Try again       │
│ Set cookie   │  │ Reset pass (opt)│
└──────────────┘  └─────────────────┘
      │
      ▼
┌────────────────────┐
│  AUTHENTICATED     │
│  Access allowed    │
│  Session valid     │
│  for 24 hours      │
└────────────────────┘
```

## Request Handling Flow

```
HTTP REQUEST
        │
        ▼
┌─────────────────────────────────────┐
│  RAILWAY LOAD BALANCER              │
│  - Route to available worker        │
│  - SSL termination                  │
│  - IP whitelist (optional)          │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │ (Multiple workers)
        ▼             ▼
    ┌──────────┐ ┌──────────┐
    │ Gunicorn │ │ Gunicorn │ ... (8 workers)
    │ Worker 1 │ │ Worker 2 │
    └────┬─────┘ └────┬─────┘
         │            │
         └────┬───────┘
              │
              ▼
      ┌──────────────────────┐
      │  Django URL Router   │
      │  - Match URL pattern │
      │  - Load view/handler │
      └──────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  VIEW FUNCTION     │
        │  - Process logic   │
        │  - Query database  │
        │  - Render template │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  RESPONSE          │
        │  - HTML/JSON       │
        │  - Status code     │
        │  - Headers         │
        └────────┬───────────┘
                 │
                 ▼
      BACK TO CLIENT ✓
```

## File Structure After Deployment

```
Railway Container
├── /app/
│   ├── PBL/                          # Project root
│   │   ├── MEDISAFE_PBL/
│   │   │   ├── settings.py           # Production settings ✓
│   │   │   ├── wsgi.py               # WSGI application
│   │   │   ├── urls.py               # URL routing
│   │   │   └── asgi.py               # ASGI application
│   │   │
│   │   ├── myapp/
│   │   │   ├── models.py             # 14 database models
│   │   │   ├── admin.py              # Django admin
│   │   │   ├── urls.py               # App URLs
│   │   │   ├── static/               # CSS, JS, images
│   │   │   ├── templates/            # HTML templates
│   │   │   ├── features/             # 10 feature modules
│   │   │   └── migrations/           # Database migrations
│   │   │
│   │   ├── staticfiles/              # Collected static files ✓
│   │   │   ├── admin/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── manifest.json
│   │   │
│   │   ├── media/                    # User uploads
│   │   │   ├── profile_photos/
│   │   │   ├── lab_pictures/
│   │   │   ├── prescriptions/
│   │   │   └── notifications/
│   │   │
│   │   ├── manage.py                 # Django CLI
│   │   ├── Procfile                  # Entry point ✓
│   │   ├── requirements.txt           # Dependencies ✓
│   │   └── runtime.txt                # Python version ✓
│   │
│   └── logs/
│       ├── gunicorn.log              # Server logs
│       ├── django.log                # Application logs
│       └── error.log                 # Error logs
│
├── /home/railway/                    # Railway system
├── /var/run/                         # Runtime files
└── /tmp/                             # Temporary files
```

## Environment Variables Mapping

```
LOCAL DEVELOPMENT                  →    RAILWAY PRODUCTION
────────────────────────────────────────────────────────────

.env file                          →    Railway Variables tab
  DJANGO_DEBUG=True                  DJANGO_DEBUG=False
  DB_HOST=localhost                  DB_HOST=containers-us-west-XXX.railway.app
  DB_NAME=local_db                   DB_NAME=railway
  DB_USER=postgres                   DB_USER=postgres
  DB_PORT=5432                       DB_PORT=5432
  (No SECRET_KEY)                    DJANGO_SECRET_KEY=[strong-key]
  (Debug mode)                       DJANGO_ALLOWED_HOSTS=yourdomain.railway.app
  No HTTPS                           (Auto HTTPS)
```

## Data Flow During File Upload

```
BROWSER
  │
  ├─► User selects file
  │   └─► Form validation (JavaScript)
  │
  ├─► POST /upload-file
  │   └─► HTTP multipart/form-data
  │
  ▼
RAILWAY LOAD BALANCER
  │
  ▼
DJANGO APP (Gunicorn Worker)
  │
  ├─► Authenticate user
  ├─► Check permissions
  ├─► Validate file type
  ├─► Validate file size
  ├─► Check for viruses (optional)
  │
  ▼
HANDLE FILE STORAGE
  │
  ├─► Persistent Volume (Option 1)
  │   └─► /app/media/
  │
  └─► AWS S3 (Option 2)
      └─► boto3 client.put_object()
  │
  ▼
DATABASE
  │
  └─► Save reference in model
      └─► UPDATE lab_results SET file='path/to/file'
  │
  ▼
RESPONSE
  │
  └─► Success: Return file URL
      Error: Return error message
  │
  ▼
BROWSER
  │
  └─► Display success/error to user
```

## Monitoring & Logging Flow

```
APPLICATION
  │
  ├─► Print statements
  ├─► Logger.info()
  ├─► Logger.error()
  └─► Exception traceback
      │
      ▼
GUNICORN STDOUT/STDERR
  │
  ▼
RAILWAY LOGS COLLECTION
  │
  ├─► Deploy Logs (visible in Railway)
  ├─► Application Logs (real-time)
  └─► Error Logs (500 errors, exceptions)
      │
      ▼
RAILWAY DASHBOARD
  │
  └─► View logs in browser
      └─► Search, filter, export
```

## Security Flow

```
HTTP REQUEST
  │
  ▼
┌──────────────────────────────┐
│ 1. FORCE HTTPS REDIRECT      │
│    DEBUG=False → REDIRECT    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 2. SSL/TLS ENCRYPTION        │
│    Railway auto SSL          │
│    All data encrypted        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 3. CSRF TOKEN VALIDATION     │
│    Check X-CSRFToken header  │
│    Validate session          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 4. AUTHENTICATION CHECK      │
│    Verify session cookie     │
│    Check user permissions    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 5. SQL INJECTION PREVENTION  │
│    Django ORM escapes all    │
│    database queries          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 6. XSS PROTECTION           │
│    Template auto-escaping    │
│    Mark safe when needed     │
└──────────┬───────────────────┘
           │
           ▼
SAFE REQUEST PROCESSING ✓
```

## Deployment Checklist Flowchart

```
┌─────────────────────────────────┐
│ START: Ready to Deploy?         │
└────────────────┬────────────────┘
                 │
         ┌───────▼───────┐
         │ All files     │
         │ created?      │
         └───┬───────┬───┘
             │ NO    │ YES
             │       └─────┐
             ▼              │
    ┌──────────────────┐    │
    │ Create:          │    │
    │ Procfile         │    │
    │ runtime.txt      │    │
    │ .gitignore       │    │
    │ .env.example     │    │
    └────┬─────────────┘    │
         │                  │
         └──────┬───────────┘
                │
         ┌──────▼──────┐
         │ Code on     │
         │ GitHub?     │
         └─┬────────┬──┘
           │ NO     │ YES
           │        └──────┐
           ▼               │
    ┌──────────────┐      │
    │ Push to      │      │
    │ GitHub       │      │
    └─────┬────────┘      │
          │               │
          └───────┬───────┘
                  │
           ┌──────▼────────┐
           │ Railway       │
           │ account       │
           │ created?      │
           └─┬──────────┬──┘
             │ NO       │ YES
             │          └──────┐
             ▼                 │
    ┌──────────────────┐      │
    │ Sign up at:      │      │
    │ railway.app      │      │
    └─────┬────────────┘      │
          │                   │
          └────┬──────────────┘
               │
        ┌──────▼──────┐
        │ Deploy!     │
        │ Watch logs  │
        │ Run migr.   │
        │ Test app    │
        └──────┬──────┘
               │
               ▼
        ✓ APP LIVE! 🚀
```

---

## Performance Optimization Tips

### For Django App
- Use database indexing (add `db_index=True` to model fields)
- Use select_related() and prefetch_related() in queries
- Add caching with Redis (optional)
- Use CDN for static files (optional)
- Monitor response times in Railway

### For Database
- Railway automatically optimizes PostgreSQL
- Enable query logging for slow queries
- Regular index maintenance
- Monitor connection pool usage

### For Static Files
- Whitenoise compresses automatically
- Browser caching headers set
- Gzip enabled by default
- No additional CDN needed (but can add Cloudflare)

### For Media Files
- Use S3 with CloudFront CDN (recommended)
- Enable versioning in Railway volume
- Set up backup strategy
- Monitor storage usage

---

## Troubleshooting Quick Reference

```
PROBLEM                    SOLUTION
─────────────────────────────────────────────────────
App won't start        →  Check Procfile
                           Check requirements.txt
                           View Railway logs

404 on CSS/JS          →  Run collectstatic
                           Check STATIC_URL

DB connection error    →  Check DB credentials
                           Verify DB_HOST
                           Test connection

Media files missing    →  Check storage solution
                           Verify permissions
                           Check file path

Login not working      →  Run migrations
                           Check SECRET_KEY
                           Clear cookies

500 errors             →  Check Django logs
                           DEBUG=False check
                           Database availability

Domain not working     →  Update ALLOWED_HOSTS
                           Check DNS records
                           Wait for propagation
```

---

## Success Indicators

When your app is properly deployed, you'll see:

✅ Green checkmark in Railway (service running)  
✅ No 500 errors in logs  
✅ CSS/JS loading without 404  
✅ Login works with credentials  
✅ Admin panel accessible  
✅ Database queries working  
✅ File uploads saved  
✅ HTTPS with padlock icon  
✅ Response time < 1 second  
✅ No "Database connection refused" errors  

---

## Architecture Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web Server** | Gunicorn | Process HTTP requests |
| **Framework** | Django 5.2.6 | Handle business logic |
| **Database** | PostgreSQL | Store data |
| **Storage** | Persistent volume/S3 | Store files |
| **Static Files** | Whitenoise | Serve CSS, JS, images |
| **Platform** | Railway | Host everything |
| **Security** | HTTPS/SSL | Encrypt data in transit |
| **Auth** | Django sessions | Manage users |

---

**You now have a complete understanding of the deployment architecture!**

Next: Read `RAILWAY_DEPLOYMENT_GUIDE.md` and follow steps 1-8.

