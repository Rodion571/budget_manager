from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Expense
from expenses.forms import ExpenseForm

User = get_user_model()

class ExpenseTests(TestCase):
    """
    Test case for the Expense model views.
    """

    def setUp(self) -> None:
        """
        Set up a test user and log them in.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_expense_list_view(self) -> None:
        """
        Test the expense list view.

        Sends a GET request to the expense list URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('expenses:expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense_list.html')

    def test_add_expense_view_post(self) -> None:
        """
        Test the add expense view POST method with invalid data.
        """
        response = self.client.post(
            reverse('expenses:add_expense'),
            {'amount': -50}
        )
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['amount'],
            ['Сума повинна бути позитивним числом.']
        )
