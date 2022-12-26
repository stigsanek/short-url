from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from short_url.links.models import Link

FAKE_URL = 'https://www.djangoproject.com/'


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
        data = {
            'target_url': 'create',
            'custom_uid': 'drf'
        }

        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 401)

        self._auth()

        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['target_url'] = FAKE_URL
        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['custom_uid'] = 'test'
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
        url_first = reverse_lazy('link-detail', args=[self.first_link.pk])
        url_second = reverse_lazy('link-detail', args=[self.second_link.pk])

        resp = self.client.put(url_second)
        self.assertEqual(resp.status_code, 401)

        self._auth()

        resp = self.client.put(url_second)
        self.assertEqual(resp.status_code, 404)

        data = {
            'target_url': FAKE_URL,
            'custom_uid': 'test',
            'name': 'test'
        }

        resp = self.client.put(path=url_first, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            Link.objects.filter(custom_uid=data['custom_uid']).exists()
        )

    def test_partial_update(self):
        url_first = reverse_lazy('link-detail', args=[self.first_link.pk])
        url_second = reverse_lazy('link-detail', args=[self.second_link.pk])

        resp = self.client.patch(url_second)
        self.assertEqual(resp.status_code, 401)

        self._auth()

        resp = self.client.patch(url_second)
        self.assertEqual(resp.status_code, 404)

        data = {
            'custom_uid': 'test',
            'name': 'test'
        }

        resp = self.client.patch(path=url_first, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            Link.objects.filter(custom_uid=data['custom_uid']).exists()
        )

    def test_destroy(self):
        url_first = reverse_lazy('link-detail', args=[self.first_link.pk])
        url_second = reverse_lazy('link-detail', args=[self.second_link.pk])

        resp = self.client.delete(url_second)
        self.assertEqual(resp.status_code, 401)

        self._auth()

        resp = self.client.delete(url_second)
        self.assertEqual(resp.status_code, 404)

        resp = self.client.delete(url_first)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            Link.objects.filter(pk=self.first_link.pk).exists()
        )
