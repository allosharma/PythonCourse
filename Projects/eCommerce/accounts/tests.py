from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationViewsTests(TestCase):
    def test_registration_page_sets_csrf_cookie(self):
        client = Client(enforce_csrf_checks=True)

        response = client.get(reverse('registration'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('csrftoken', response.cookies)

    def test_login_page_sets_csrf_cookie(self):
        client = Client(enforce_csrf_checks=True)

        response = client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('csrftoken', response.cookies)

    def test_registration_blocks_duplicate_email(self):
        User.objects.create_user(
            username='9999999999',
            email='taken@example.com',
            password='secret123',
        )

        response = self.client.post(
            reverse('registration'),
            {
                'first_name': 'Aman',
                'last_name': 'Sharma',
                'phone_number': '8888888888',
                'email': 'taken@example.com',
                'password': 'secret123',
            },
        )

        self.assertRedirects(response, reverse('registration'))
        self.assertEqual(User.objects.filter(email='taken@example.com').count(), 1)

    def test_login_redirects_home_for_valid_credentials(self):
        User.objects.create_user(
            username='9999999999',
            email='user@example.com',
            password='secret123',
        )

        response = self.client.post(
            reverse('login'),
            {
                'phone_number': '9999999999',
                'password': 'secret123',
            },
        )

        self.assertRedirects(response, reverse('home'))

    def test_logout_requires_post(self):
        user = User.objects.create_user(
            username='9999999999',
            email='user@example.com',
            password='secret123',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)
