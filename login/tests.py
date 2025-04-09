from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticTest(TestCase):
    def setUp(self):
        # This runs before each test method
        self.username = 'testuser'
        self.password = 'testpass123'
        self.email = 'test@example.com'
        User.objects.create_user(username=self.username, password=self.password, email=self.email)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            "username": self.username,
            "password": self.password,
        })
        self.assertRedirects(response, reverse('home'))

    def test_signup_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "abc123",
            "password2": "xyz456",
        })
        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(User.objects.filter(username="newuser").exists())
