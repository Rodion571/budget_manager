from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse


class NewAppTests(TestCase):
    """
    Test case for the New App views.

    Methods:
        test_index_view(): Test the index view.
    """

    def test_index_view(self) -> None:
        """
        Test the index view.

        Sends a GET request to the index URL.

        Asserts:
            The response status code is 200.
            The response contains the expected content.
        """
        response: HttpResponse = self.client.get(reverse('new_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the New App')
