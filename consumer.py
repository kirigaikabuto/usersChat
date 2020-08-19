from kafka import KafkaConsumer
import json
from django.conf import settings
import mysite.settings as app_settings
settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
import django
django.setup()
from chat.models import Chat
from django.contrib.auth.models import User



bootstrap_servers = ['localhost:9092']
topicName = 'user1_user2'
consumer = KafkaConsumer(topicName, group_id='group2', bootstrap_servers=bootstrap_servers, auto_offset_reset="earliest")
for msg in consumer:
    data = json.loads(msg.value)
    user1 = User.objects.get(username=data['from_user'])
    user2 = User.objects.get(username=data['to_user'])
    chat = Chat(chat_id=topicName, from_user = user1,to_user=user2, message= data['message'])
    chat.save()
    print(chat)
    consumer.commit()