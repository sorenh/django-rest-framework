from django.conf.urls import include, url
from django.db import models
from rest_framework.test import APITestCase

from rest_framework import permissions, serializers, viewsets
from rest_framework.routers import SimpleRouter

class Item(models.Model):
    name = models.CharField(max_length=200)

class Bucket(models.Model):
    items = models.ManyToManyField(Item)

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('name',)

class BucketSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.HyperlinkedRelatedField(many=True, view_name='item-detail', queryset=Item.objects.all())

    class Meta:
        model = Bucket
        fields = ('items',)

class BucketViewSet(viewsets.ModelViewSet):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    permission_classes = [permissions.AllowAny]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]

router = SimpleRouter()
router.register(r'buckets', BucketViewSet)
router.register(r'items', BucketViewSet)

urlpatterns = [url(r'', include(router.urls))]


class TestMyProblem(APITestCase):
    urls = 'tests.test_mything'

    def test_create_bucket(self):
        response = self.client.post('/buckets/', {}, format='json')
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {'items': ['This field is required.']})

    def test_create_bucket_empty_body(self):
        response = self.client.post('/buckets/')
        self.assertEquals(response.status_code, 201)
