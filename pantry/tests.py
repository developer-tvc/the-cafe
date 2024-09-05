from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from .models import AboutCafe

class CafeModelTestCase(TestCase):

    def setUp(self):
        # This method is run before each test
        AboutCafe.objects.create(cafe_name="J5 - the Coffee Shop and Espresso Bar- the CaFe", about="A test model description for AboutCafe")

    def test_model_str(self):
        # Test the __str__ method of the model
        model = AboutCafe.objects.get(cafe_name="J5 - the Coffee Shop and Espresso Bar- the CaFe")
        self.assertEqual(str(model), model.cafe_name)
    

    def test_redirect_if_not_logged_in(self):
        # Ensure the client is logged out
        self.client.logout()
        # Access the protected view
        response = self.client.get(reverse('login'))
        # Build the expected redirect URL
        login_url = 'login/'+'?next=' + reverse('login')
        # Assert that the response is a redirect to the login page
        self.assertRedirects(response, login_url)

    
    def test_logged_in_user_can_access(self):
        # Log in the test user
        self.client.login(username='namitha@techversantinfo.com', password='namitha@login2021')
        # Now access the protected view
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        

    def test_model_not_found(self):
        # Test for a non-existent model detail
        url = reverse('mymenu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class MyModelAPITestCase(APITestCase):

    def setUp(self):
        self.model = AboutCafe.objects.create(cafe_name="J5 - the Coffee Shop and Espresso Bar- the CaFe", about="A test model description for AboutCafe")
        self.url = reverse('login')

    def test_get_mymodel(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)