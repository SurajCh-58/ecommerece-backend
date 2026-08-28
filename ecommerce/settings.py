"""
Django settings for ecommerce project.
"""
import base64
from pathlib import Path
import os
import environ

# ==============================================================================
# ENVIRONMENT & BASE DIRECTORY SETUP
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ==============================================================================
# CORE DJANGO CONFIGURATION
# ==============================================================================

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

ROOT_URLCONF = 'ecommerce.urls'
WSGI_APPLICATION = 'ecommerce.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.headless',

    # Local
    'accounts.apps.AccountsConfig',
    'products',
    'cart',
    'orders',
    'payment'
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # CorsMiddleware must be as high as possible, before any middleware
    # that can generate responses such as CommonMiddleware.
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # CSRF middleware is kept intentionally.
    # allauth automatically applies @csrf_exempt to all /_allauth/app/v1/* endpoints,
    # so Postman/API calls are never blocked by CSRF.
    # This middleware stays to protect the Django admin panel.
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================================================================
# TEMPLATES
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================================================================
# AUTHENTICATION & USER MODEL
# ==============================================================================

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    # Handles admin login and direct authenticate() calls.
    'django.contrib.auth.backends.ModelBackend',

    # Handles allauth email login and all allauth-specific flows.
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================

# NOTE: No frontend connected yet — these are placeholder origins.
# Add your actual frontend domain here when ready.
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:3000',
    'http://localhost:5500',
    'http://localhost:8000',
])

CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# DJANGO REST FRAMEWORK
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Reads JWT from Authorization: Bearer <token> header.
        'allauth.headless.contrib.rest_framework.authentication.JWTTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
}

# ==============================================================================
# DJANGO ALLAUTH — Account Configuration
# ==============================================================================

# Only email login — no username.
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# 'mandatory' — must verify email before login.
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*']

# False = tells user if email already registered.
# TODO: set True in production to prevent email enumeration attacks.
ACCOUNT_EMAIL_ENUMERATE = False

# ── Email OTP ─────────────────────────────────────────────────────────────────
# Sends a 6-digit code instead of a magic link.
# User submits code to: POST /_allauth/app/v1/auth/email/verify
# allauth expects plain integers (seconds) for timeout — NOT timedelta.
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_MAX_ATTEMPTS = 5
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_TIMEOUT = 600   # 10 minutes in seconds (int, not timedelta)
ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_RESEND = True

# ── Password Reset OTP ────────────────────────────────────────────────────────
# allauth expects plain integers (seconds) for timeout — NOT timedelta.
ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED = True
ACCOUNT_PASSWORD_RESET_TOKEN_FLOW = 'code'
ACCOUNT_PASSWORD_RESET_BY_CODE_MAX_ATTEMPTS = 5
ACCOUNT_PASSWORD_RESET_BY_CODE_TIMEOUT = 900       # 15 minutes in seconds (int, not timedelta)
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

# Custom adapter
ACCOUNT_ADAPTER = 'accounts.adapter.CustomAccountAdapter'

# ==============================================================================
# DJANGO ALLAUTH — Headless Configuration
# ==============================================================================

# 'app' = stateless JWT mode for APIs/Postman/mobile.
HEADLESS_CLIENTS = ('app',)

# Tells allauth this project has NO traditional browser views.
# Without this, allauth tries to redirect to URL names like
# 'account_email_verification_sent' after signup — which don't exist
# in a headless-only project — causing NoReverseMatch errors.
# With this set, allauth stays in pure JSON/API mode throughout.
HEADLESS_ONLY = True

HEADLESS_TOKEN_STRATEGY = 'allauth.headless.tokens.strategies.jwt.JWTTokenStrategy'

# Private key stored as base64 in .env to avoid newline issues.
# Generate with: openssl genpkey -algorithm ed25519 | base64 -w 0
# Then set: ALLAUTH_JWT_PRIVATE_KEY_B64=<output> in .env
b64_key = env('ALLAUTH_JWT_PRIVATE_KEY_B64', default=None)
if b64_key:
    HEADLESS_JWT_PRIVATE_KEY = base64.b64decode(b64_key).decode('utf-8')
else:
    HEADLESS_JWT_PRIVATE_KEY = None

HEADLESS_JWT_ALGORITHM = 'RS256'

# allauth expects plain integers (seconds) for JWT expiry — NOT timedelta.
HEADLESS_JWT_ACCESS_TOKEN_EXPIRES_IN = 7200         # 15 minutes in seconds (int, not timedelta)
HEADLESS_JWT_REFRESH_TOKEN_EXPIRES_IN = 604800     # 7 days in seconds (int, not timedelta)
HEADLESS_JWT_ROTATE_REFRESH_TOKEN = True

# Validates JWT against DB on every request — allows server-side revocation.
# Set False for pure stateless JWT (faster but tokens can't be revoked).
HEADLESS_JWT_STATEFUL_VALIDATION_ENABLED = True

# ── Frontend URLs ─────────────────────────────────────────────────────────────
# NOTE: No frontend connected yet — placeholder URLs.
# Since OTP codes are used (not magic links), these only appear
# as fallbacks in emails and don't affect the Postman/API flow at all.
# Replace with actual frontend URLs when frontend is connected.
HEADLESS_FRONTEND_URLS = {
    'account_confirm_email': 'http://localhost:3000/auth/verify-email/{key}',
    'account_reset_password_from_key': 'http://localhost:3000/auth/password/reset/{key}',
}

# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    # Format in .env: DATABASE_URL=postgres://user:password@host:port/dbname
    'default': env.db()
}

# ==============================================================================
# EMAIL
# ==============================================================================

# Console backend prints emails to terminal — good for development.
# Switch to SMTP in production by setting EMAIL_BACKEND in .env:
#   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
#   EMAIL_HOST=smtp.sendgrid.net
#   EMAIL_PORT=587
#   EMAIL_USE_TLS=True
#   EMAIL_HOST_USER=your@email.com
#   EMAIL_HOST_PASSWORD=yourpassword
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# ==============================================================================
# INTERNATIONALIZATION & TIMEZONE
# ==============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# JAZZMIN ADMIN UI
# ==============================================================================

JAZZMIN_SETTINGS = {
    'site_title': 'Ecommerce Admin',
    'site_header': 'Ecommerce',
    'site_brand': 'Ecommerce Admin',
    'welcome_sign': 'Welcome to Dashboard',
    'show_sidebar': True,
    'navigation_expanded': True,
    'hide_apps': ['auth'],
    'hide_models': ['auth.Group'],
    'order_with_respect_to': ['auth', 'store.Product'],
    'copyright': 'Your Company Name Ltd',
    'show_ui_builder': True,
    'custom_css': 'css/custom_admin.css',
}

# ==============================================================================
# PRODUCTION SECURITY FLAGS
# ==============================================================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

# TEMPORARY DEBUG — remove before production
if DEBUG:
    if HEADLESS_JWT_PRIVATE_KEY:
        print("✓ JWT private key loaded successfully")
        print(f"  Key starts with: {HEADLESS_JWT_PRIVATE_KEY[:27]}")  # should show -----BEGIN PRIVATE KEY
    else:
        print("✗ JWT private key is None — check ALLAUTH_JWT_PRIVATE_KEY_B64 in .env")