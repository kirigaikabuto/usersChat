from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    chat_id = models.CharField(max_length=255)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    message = models.TextField()

    def __str__(self):
        return self.from_user.username+"->"+self.to_user.username