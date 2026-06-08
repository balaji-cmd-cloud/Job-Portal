import json
from django.http import JsonResponse
from .models import ChatHistory
from .chatbot_logic import get_chatbot_response

def chatbot_api_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not message:
            return JsonResponse({'error': 'Message is empty'}, status=400)

        user = request.user if request.user.is_authenticated else None
        response = get_chatbot_response(message, user)

        # Persist conversation in ChatHistory model
        ChatHistory.objects.create(
            user=user,
            user_message=message,
            bot_response=response
        )

        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

