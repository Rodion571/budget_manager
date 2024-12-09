from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class IncomesTests(TestCase):
    """
    Test case for the Incomes views.

    Methods:
        test_add_income_view(): Test the add income view.
        test_add_income_view_post(): Test the add income view with POST.
        test_income_list_view(): Test the income list view.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        Creates a test user.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_add_income_view(self) -> None:
        """
        Test the add income view.

        Sends a GET request to the add income URL.

        Asserts:
            The response status code is 200.
        """
        self.client.login(username='testuser', password='testpassword')
        response: HttpResponse = self.client.get(reverse('add_income'))
        self.assertEqual(response.status_code, 200)

    def test_add_income_view_post(self) -> None:
        """
        Test the add income view with POST.

        Sends a POST request to the add income URL.

        Asserts:
            The response status code is 302 if the form is valid, otherwise check for form errors.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_income'), {
            'name': 'Test Income',
            'source': 'Test Source',
            'amount': 100,
            'date': '2024-12-09',
        })
        if response.status_code == 200:
            print(response.content.decode())
            form_errors = response.context['form'].errors
            print(f"Form errors: {form_errors}")
            self.fail("Форма не прошла валидацию. Проверьте содержимое ответа для ошибок.")
        else:
            self.assertEqual(response.status_code, 302)

    def test_income_list_view(self) -> None:
        """
        Test the income list view.

        Sends a GET request to the income list URL.

        Asserts:
            The response status code is 200.
        """
        self.client.login(username='testuser', password='testpassword')
        response: HttpResponse = self.client.get(reverse('income_list'))
        self.assertEqual(response.status_code, 200)
