from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from short_url.links.models import Link


class TestRedirect(APITestCase):
    """Tests for redirect"""
    fixtures = ['users.json', 'links.json']

    def test_redirect(self):
        link = Link.objects.get(pk=1)
        url_first = reverse_lazy('redirect', args=[link.uid])
        url_second = reverse_lazy('redirect', args=[link.custom_uid])

        resp = self.client.post(url_first)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.get(url_first)
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(url_second)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Link.objects.get(pk=1).click_count, 2)

        resp = self.client.get(reverse_lazy('redirect', args=['test']))
        self.assertEqual(resp.status_code, 404)
