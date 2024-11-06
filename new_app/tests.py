from django.test import TestCase
from django.urls import reverse

class NewAppTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('new_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the New App')
