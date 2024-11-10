from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Budget

class HomeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_home_content_view(self):
        response = self.client.get(reverse('home:home_content'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_expense_list_view(self):
        response = self.client.get(reverse('home:expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense_list.html')

    def test_add_expense_view(self):
        response = self.client.get(reverse('home:add_expense'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_expense.html')

    def test_add_income_view(self):
        response = self.client.get(reverse('home:add_income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/add_income.html')

    def test_budget_planning_view(self):
        response = self.client.get(reverse('home:budget_planning'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget_planning.html')

    def test_budget_model(self):
        budget = Budget.objects.create(
            name="New Budget",
            category="Доход",
            amount=200.00,
            date="2024-11-07"
        )
        self.assertEqual(str(budget), "New Budget - Доход: 200.00 on 2024-11-07")
