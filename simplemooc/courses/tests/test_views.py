from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from courses.models import Course

class ContactCourseTestCase(TestCase):

    # vai rodar toda vez que o teste for executado
    # setUp roda no inicio do teste
    def setUp(self):
        self.course = Course.objects.create(name='Django', slug='django')

    # tearDown roda no fim do teste
    def tearDown(self):
        self.course.delete()

    # Teste para quando ocorrer um erro
    def test_contact_form_error(self):
        data = {'name': 'Fulano de Tal', 'email':'', 'message':''}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    # Teste para quando dat certo
    def test_contact_forms_sucess(self):
        data = {'name': 'Fulano de Tal', 'email':'fulango@gmail.com', 'message':'Isso é apenas um teste'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])