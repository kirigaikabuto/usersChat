from kafka import KafkaConsumer
import json
from django.conf import settings
import mysite.settings as app_settings
settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
import django
django.setup()
from chat.models import Chat
from django.contrib.auth.models import User



