from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class ChatbotAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.admin = get_user_model().objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.client.login(username='testuser', password='testpass')

    def test_send_message(self):
        # Test sending a message to the admin
        url = reverse('message-list')  # Reverse the URL name for the router endpoint
        data = {
            "receiver": self.admin.id,
            "text": "Hello Admin!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_messages(self):
        # Test getting messages for a user
        url = reverse('message-list')  # Adjust based on the route
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
