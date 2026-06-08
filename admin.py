from django.contrib import admin
from .models import ChatHistory

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message_excerpt', 'bot_response_excerpt', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__email', 'user_message', 'bot_response')

    def user_message_excerpt(self, obj):
        return obj.user_message[:50] + '...' if len(obj.user_message) > 50 else obj.user_message
    user_message_excerpt.short_description = 'User Message'

    def bot_response_excerpt(self, obj):
        return obj.bot_response[:50] + '...' if len(obj.bot_response) > 50 else obj.bot_response
    bot_response_excerpt.short_description = 'Bot Response'

