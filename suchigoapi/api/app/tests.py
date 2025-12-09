from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile, Bill, Pickup, Address
from datetime import datetime, timedelta

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())

    def test_login_user(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_profile_update(self):
        self.client.post(self.register_url, self.user_data)
        login_response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        profile_url = reverse('profile')
        update_data = {'phone_number': '1234567890'}
        response = self.client.patch(profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '1234567890')

    def test_create_bill(self):
        self.client.post(self.register_url, self.user_data)
        login_response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        bill_url = reverse('bill-list')
        bill_data = {
            'amount': '100.00',
            'due_date': '2023-12-31',
            'description': 'Test Bill'
        }
        response = self.client.post(bill_url, bill_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bill.objects.count(), 1)

    def test_create_pickup(self):
        self.client.post(self.register_url, self.user_data)
        login_response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        pickup_url = reverse('pickup-list')
        # Use a future date for the scheduled_date
        future_date = datetime.now() + timedelta(days=7)
        pickup_data = {
            'scheduled_date': future_date.isoformat(),
            'items_description': 'Test Items',
            'pickup_address': 'Test Address'
        }
        response = self.client.post(pickup_url, pickup_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pickup.objects.count(), 1)