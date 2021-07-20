from django.test import TestCase, Client
from django.test.client import encode_multipart
from .models import Collection, Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class CollectionEndpoint(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username="user_a", email="usera@techface.ch")
        self.collection_a = Collection.objects.create(
            name="collection_a", owner=self.user_a)

        self.user_b = User.objects.create_user(
            username="user_b", email="userb@techface.ch")
        self.collection_b = Collection.objects.create(
            name="collection_b", owner=self.user_b)

    def test_endpoint_collections_requires_login(self):
        c = Client()
        response = c.get('/api/collections/')

        self.assertEqual(response.status_code, 401)

    def test_endpoint_collections_only_shows_users_collection(self):
        c = Client()
        c.force_login(self.user_a)
        response = c.get('/api/collections/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_endpoint_collections_serializes_name(self):
        c = Client()
        c.force_login(self.user_a)
        response = c.get(f'/api/collections/{self.collection_a.id}/')

        self.assertEqual(response.json()['name'], self.collection_a.name)
