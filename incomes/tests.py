from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Income

User = get_user_model()

class IncomeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_income_list_view(self):
        response = self.client.get(reverse('incomes:income_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income_list.html')

    def test_add_income_view(self):
        response = self.client.get(reverse('incomes:add_income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/add_income.html')
