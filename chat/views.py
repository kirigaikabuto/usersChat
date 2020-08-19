from django.shortcuts import render
from django.contrib.auth.models import User
import json
from kafka import KafkaProducer
from .models import Chat


def chat_page(request):
    user1 = request.user
    #user2 = User.objects.get(pk=id)
    user2 = User.objects.get(username="user1")
    # topic_name = user1.username + "_" + user2.username
    topic_name = "user1_user2"
    if request.method == "POST":
        message = request.POST['message']
        message_dict = {
            "from_user": user1.username,
            "to_user": user2.username,
            "message": message,
        }
        message_json = json.dumps(message_dict)
        bootstrap_servers = ['localhost:9092']
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        producer.send(topic_name, bytearray(message_json, 'utf-8'))
        producer.flush()
    chat = Chat.objects.filter(chat_id=topic_name,).all()

    context = {
        "chat":chat
    }
    return render(request, "chat/chat.html", context=context)
