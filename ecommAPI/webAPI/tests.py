from django.test import TestCase
from .models import BDetect as BDetectCookie  # Import the model classes we just wrote.

# Create your tests here.

print(dict(cookie) for cookie in list(BDetectCookie.objects.values()))