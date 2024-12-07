from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

class UserRegistrationTestCase(TestCase):
    """
    Test case for user registration.

    Methods:
        test_register_user(): Test registering a new user.
        test_register_user_invalid_date(): Test registering a new user with an invalid date of birth.
    """

    def test_register_user(self) -> None:
        """
        Test registering a new user.

        Sends a POST request to the registration URL with user data.

        Asserts:
            The response status code is 302 (redirect).
            The new user exists in the database.
        """
        response: HttpResponse = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword',
            'password2': 'complexpassword',
            'date_of_birth': '1990-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_invalid_date(self) -> None:
        """
        Test registering a new user with an invalid date of birth.

        Sends a POST request to the registration URL with invalid date of birth.

        Asserts:
            The response status code is 200 (no redirect).
            The error message is returned.
        """
        response: HttpResponse = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword',
            'password2': 'complexpassword',
            'date_of_birth': '3000-01-01'  # Invalid date
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFormError(form, 'date_of_birth', 'Невірний рік, такої дати немає.')

class UserLoginTestCase(TestCase):
    """
    Test case for user login.

    Methods:
        setUp(): Set up a test user.
        test_login_user(): Test logging in an existing user.
    """

    def setUp(self) -> None:
        """
        Set up a test user.
        """
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_login_user(self) -> None:
        """
        Test logging in an existing user.

        Sends a POST request to the login URL with user credentials.

        Asserts:
            The response status code is 302 (redirect).
            The redirection URL is the home content page.
        """
        response: HttpResponse = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home_content'))
