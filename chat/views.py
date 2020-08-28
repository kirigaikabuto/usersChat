from django.shortcuts import render
from django.contrib.auth.models import User
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from .models import Chat
#topic->user1_user2
#topic->user2_user1

def chat_page(request, user2_pk):
    user1 = request.user
    user2 = User.objects.get(pk=user2_pk)
    # topic_name = user1.username + "_" + user2.username
    topic_name = user1.username + "_" + user2.username
    obj1 = Chat.objects.filter(from_user=user1, to_user=user2)
    if len(obj1) != 0:
        topic_name = obj1[0].chat_id
    obj2 = Chat.objects.filter(from_user=user2, to_user=user1)
    if len(obj2) !=0:
        topic_name = obj2[0].chat_id

    print(topic_name)
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

        myKakfaConsumer(topic_name)
    chat = Chat.objects.filter(chat_id=topic_name,).all()

    context = {
        "chat":chat
    }
    return render(request, "chat/chat.html", context=context)


def myKakfaConsumer(topicName):
    bootstrap_servers = ['localhost:9092']
    consumer = KafkaConsumer(topicName, group_id='group2', bootstrap_servers=bootstrap_servers,
                             auto_offset_reset="earliest", consumer_timeout_ms=1000)
    for msg in consumer:
        print("start reading")
        data = json.loads(msg.value)
        user1 = User.objects.get(username=data['from_user'])
        user2 = User.objects.get(username=data['to_user'])
        chat = Chat(chat_id=topicName, from_user=user1, to_user=user2, message=data['message'])
        chat.save()
        consumer.commit()
    print("end consumer")