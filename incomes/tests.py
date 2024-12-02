from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Income
from incomes.forms import IncomeForm

User = get_user_model()

class IncomeTests(TestCase):
    """
    Test case for the Income model views.
    """

    def setUp(self) -> None:
        """
        Set up a test user and log them in.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_income_list_view(self) -> None:
        """
        Test the income list view.

        Sends a GET request to the income list URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('incomes:income_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income_list.html')

    def test_add_income_view(self) -> None:
        """
        Test the add income view.

        Sends a GET request to the add income URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('incomes:add_income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/add_income.html')

    def test_add_income_view_post(self) -> None:
        """
        Test the add income view POST method with invalid data.
        """
        response = self.client.post(reverse('incomes:add_income'), {
            'name': 'Test Income',
            'source': 'Job',
            'amount': -100,
            'date': '2024-12-02'
        })
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['amount'], ['Сума повинна бути позитивним числом.'])
