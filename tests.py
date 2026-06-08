from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ChatHistory
from .chatbot_logic import get_chatbot_response

User = get_user_model()

class ChatbotTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='chatty@example.com',
            password='Password123!',
            first_name='Chatty'
        )

    def test_chatbot_logic_greetings(self):
        response = get_chatbot_response('Hello there!', self.user)
        self.assertIn('AI Career Assistant', response)
        self.assertIn('Chatty', response)

    def test_chatbot_logic_skills(self):
        response = get_chatbot_response('what are the trending skills?')
        self.assertIn('skills', response)
        self.assertIn('in-demand', response)

    def test_chatbot_api_endpoint(self):
        url = reverse('chatbot_api')
        
        # Test greeting input
        response = self.client.post(
            url,
            {'message': 'hi'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('AI Career Assistant', data['response'])
        
        # Verify history is logged
        self.assertEqual(ChatHistory.objects.count(), 1)
        chat = ChatHistory.objects.first()
        self.assertEqual(chat.user_message, 'hi')
        self.assertIn('AI Career Assistant', chat.bot_response)

