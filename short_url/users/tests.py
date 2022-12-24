from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

FAKE_PASSWORD = 'Fake_pass1!2@'


class TestUsers(APITestCase):
    """Tests for users"""
    fixtures = ['users.json']

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.first_user_token = Token.objects.create(user=self.first_user)

    def _auth(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.first_user_token.key
        )

    def test_auth_token(self):
        url = reverse_lazy('auth-token')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 405)

        data = {
            'username': self.first_user.username,
            'password': FAKE_PASSWORD
        }

        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.first_user_token.key, resp.json()['token'])

        data['username'] = self.second_user.username
        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.json())

    def test_list(self):
        url = reverse_lazy('user-list')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

        self._auth()
        resp = self.client.get(url)
        data = resp.json()['results']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['username'], self.first_user.username)
        self.assertEqual(data[1]['username'], self.second_user.username)

    def test_create(self):
        url = reverse_lazy('user-list')
        data = {
            'username': 'create',
            'password': 'test'
        }

        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['password'] = FAKE_PASSWORD
        resp = self.client.post(path=url, data=data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            User.objects.filter(username='create').exists()
        )

    def test_detail(self):
        url_first = reverse_lazy('user-detail', args=[self.first_user.pk])
        url_second = reverse_lazy('user-detail', args=[self.second_user.pk])

        resp = self.client.get(url_first)
        self.assertEqual(resp.status_code, 401)

        self._auth()
        resp = self.client.get(url_first)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['username'], self.first_user.username)

        resp = self.client.get(url_second)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['username'], self.second_user.username)

    def test_update(self):
        url_first = reverse_lazy('user-detail', args=[self.first_user.pk])
        url_second = reverse_lazy('user-detail', args=[self.second_user.pk])

        resp = self.client.put(url_first)
        self.assertEqual(resp.status_code, 401)

        self._auth()
        data = {
            'username': 'update',
            'password': FAKE_PASSWORD
        }

        resp = self.client.put(path=url_second, data=data)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.put(path=url_first, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            User.objects.filter(username='update').exists()
        )

    def test_partial_update(self):
        url_first = reverse_lazy('user-detail', args=[self.first_user.pk])
        url_second = reverse_lazy('user-detail', args=[self.second_user.pk])

        resp = self.client.patch(url_first)
        self.assertEqual(resp.status_code, 401)

        self._auth()
        data = {
            'username': 'partial_update',
            'password': FAKE_PASSWORD
        }

        resp = self.client.patch(path=url_second, data=data)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.put(path=url_first, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            User.objects.filter(username='partial_update').exists()
        )

    def test_destroy(self):
        url_first = reverse_lazy('user-detail', args=[self.first_user.pk])
        url_second = reverse_lazy('user-detail', args=[self.second_user.pk])

        resp = self.client.delete(url_first)
        self.assertEqual(resp.status_code, 401)

        self._auth()

        resp = self.client.delete(url_second)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(url_first)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            User.objects.filter(username=self.first_user.username).exists()
        )
