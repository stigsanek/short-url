from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from short_url.links.models import Link


class TestLinks(APITestCase):
    """Tests for links"""
    fixtures = ['users.json', 'links.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.first_link = Link.objects.get(pk=1)
        self.second_link = Link.objects.get(pk=2)

    def _auth(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key
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
        url = reverse_lazy('link-list')
        data = {'target_url': 'create'}

        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 401)

        self._auth()

        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['target_url'] = 'https://www.djangoproject.com/'
        resp = self.client.post(path=url, data=data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            Link.objects.filter(target_url=data['target_url']).exists()
        )

    def test_detail(self):
        url_first = reverse_lazy('link-detail', args=[self.first_link.pk])
        url_second = reverse_lazy('link-detail', args=[self.second_link.pk])

        resp = self.client.get(url_second)
        self.assertEqual(resp.status_code, 401)

        self._auth()

        resp = self.client.get(url_second)
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(url_first)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['name'], self.first_link.name)

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass
