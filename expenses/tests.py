from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Expense  # Импортируем модель Expense

class ExpenseTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_expense_list_view(self):
        response = self.client.get(reverse('expenses:expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense_list.html')

    def test_add_expense_view(self):
        response = self.client.get(reverse('expenses:add_expense'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_expense.html')
