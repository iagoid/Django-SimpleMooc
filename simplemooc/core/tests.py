from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class HomeViewTest(TestCase):

    def test_home_status_code(self):
        client = Client()
        # Recebe a URL do home
        response = client.get(reverse('core:home'))
        # O teste que será feito
        self.assertEqual(response.status_code, 200)
    
    def test_home_template_used(self):
        client = Client()
        # Recebe a URL do home
        response = client.get(reverse('core:home'))
        # O teste que será feito(templates que são usados)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertTemplateUsed(response, 'base.html')


