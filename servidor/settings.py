# Django settings for servidor project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Daniel', 'drobles@econain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'econadmin',
        'USER': 'django',
        'PASSWORD': 'spedatha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
TIME_ZONE = 'America/Lima'
LANGUAGE_CODE = 'es-PE'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = '/home/econain/Django/econadmin2v0/servidor/media/'
MEDIA_URL = 'http://local.econadmin/media/'
STATIC_ROOT = '/home/econain/Django/econadmin2v0/servidor/static/'
STATIC_URL = 'http://local.econadmin/media/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = '46dnhoq@ijwzsapb*7+f%chmx38*+o8&amp;&amp;*x_$9av^sjt$@563$'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
X_FRAME_OPTIONS = 'DENY'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'servidor.urls'
WSGI_APPLICATION = 'servidor.wsgi.application'
TEMPLATE_DIRS = (
    '/home/econain/Django/econadmin2v0/servidor/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
