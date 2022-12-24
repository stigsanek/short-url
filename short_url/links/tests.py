from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from short_url.links.models import Link


class TestLinks(APITestCase):
    """Tests for links"""
    fixtures = ['users.json', 'links.json']

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.first_user_token = Token.objects.create(user=self.first_user)

        self.first_link = Link.objects.get(pk=1)
        self.second_link = Link.objects.get(pk=1)

    def _auth(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.first_user_token.key
        )

    def test_list(self):
        url = reverse_lazy('link-list')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

        self._auth()
        resp = self.client.get(url)
        data = resp.json()['results']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['target_url'], self.first_link.target_url)

    def test_create(self):
        pass

    def test_detail(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass
