import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FuelProject.settings')
os.environ.setdefault('TESTING', 'True')
os.environ.setdefault('SECRET_KEY', 'django-insecure-test-key')


try:
    import django
except ImportError:
    django = None


if django is not None:
    django.setup()