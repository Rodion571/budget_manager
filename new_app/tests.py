from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class NewAppTests(TestCase):
    """
    Test case for the New App views.

    Methods:
        test_index_view(): Test the index view.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        Creates a test user.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self) -> None:
        """
        Test the index view.

        Sends a GET request to the index URL.

        Asserts:
            The response status code is 200.
            The response contains the expected content.
        """
        self.client.login(username='testuser', password='testpassword')
        response: HttpResponse = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the New App')
