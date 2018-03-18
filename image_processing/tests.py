from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

import json


class ImageProcessingTest(APITestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self.url = reverse('process_image')

    def test_image_upload(self):
        image = ''
        res = self.client.post(self.url, image)
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)

    def test_image_listing(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class ProcessedImageTest(APITestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self.url = reverse('process_image') + 'test'

    def test_image_progress(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
