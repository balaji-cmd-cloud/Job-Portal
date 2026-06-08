from django.db import models
from django.conf import settings

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_histories')
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name_plural = "Chat Histories"

    def __str__(self):
        user_email = self.user.email if self.user else "Anonymous"
        return f"Chat by {user_email} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

