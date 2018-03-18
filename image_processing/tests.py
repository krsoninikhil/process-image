from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

import json


class ImageProcessingTest(APITestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self.url = reverse('process_image')

    def test_image_upload(self):
        with open('media/test_images/nn-271x201.png', 'rb') as image:
            res = self.client.post(self.url, {'image': image})
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)

    def test_invalid_image_upload(self):
        with open('media/test_images/nn-201x149.png', 'rb') as image:
            res = self.client.post(self.url, {'image': image})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_listing(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
