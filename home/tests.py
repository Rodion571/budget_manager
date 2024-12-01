from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Budget

User = get_user_model()


class HomeTests(TestCase):
    """
    Test case for the home views and budget model.

    Methods:
        setUp(): Set up a test user and log them in.
        test_home_content_view(): Test the home content view.
        test_expense_list_view(): Test the expense list view.
        test_add_expense_view(): Test the add expense view.
        test_add_income_view(): Test the add income view.
        test_budget_planning_view(): Test the budget planning view.
        test_budget_model(): Test the budget model representation.
    """

    def setUp(self) -> None:
        """
        Set up a test user and log them in.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_home_content_view(self) -> None:
        """
        Test the home content view.

        Sends a GET request to the home content URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('home:home_content'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_expense_list_view(self) -> None:
        """
        Test the expense list view.

        Sends a GET request to the expense list URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('home:expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense_list.html')

    def test_add_expense_view(self) -> None:
        """
        Test the add expense view.

        Sends a GET request to the add expense URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('home:add_expense'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_expense.html')

    def test_add_income_view(self) -> None:
        """
        Test the add income view.

        Sends a GET request to the add income URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('home:add_income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/add_income.html')

    def test_budget_planning_view(self) -> None:
        """
        Test the budget planning view.

        Sends a GET request to the budget planning URL.

        Asserts:
            The response status code is 200.
            The correct template is used for the response.
        """
        response: HttpResponse = self.client.get(reverse('home:budget_planning'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget_planning.html')

    def test_budget_model(self) -> None:
        """
        Test the budget model representation.

        Creates a budget instance and checks its string representation.

        Asserts:
            The string representation of the budget is correct.
        """
        budget = Budget.objects.create(
            name="New Budget",
            category="Доход",
            amount=200.00,
            date="2024-11-07"
        )
        self.assertEqual(str(budget), "New Budget - Доход: 200.00 on 2024-11-07")
