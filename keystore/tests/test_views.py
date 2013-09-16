import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from keys.models import KeyPair
from factories import UserFactory, KeyPairFactory
from django.contrib.auth.models import User

class KeyPairAPITests(TestCase):

    def setUp(self):
        self.test_user = UserFactory()
        print KeyPairFactory(user=self.test_user)
    def test_list(self):
        url = reverse("keys.views.keypair_api_general")
        print self.client.login(username=self.test_user.username,password='password')
        response = self.client.get(url,follow=True)
        self.assertEquals(response.status_code, 200)
        print response.content, KeyPair.objects.count()
        data = json.loads(response.content)

        self.assertEquals(len(data), 1)
