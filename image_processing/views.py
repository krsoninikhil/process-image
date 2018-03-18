from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import time
import random
import threading
from  image_processing.models import UploadedImage, process_uploaded_image

MIME_WHITELIST = ['image/png', 'image/jpeg', 'image/jpg']


class ImageProcessing(APIView):
    ''' Interface to image processing functions. '''

    def post(self, request):
        ''' To upload the image. Returns the url to check progress. '''

        # get the uploaded image
        uploaded_image = request.FILES.get('image')
        if uploaded_image is None:
            res_body = {'error': 'No image found!'}
            return Response(res_body, status=status.HTTP_400_BAD_REQUEST)

        # change the name of image
        name = '{}_{}'.format(time.time(), random.random())
        uploaded_image.name = '{}.{}'.format(name,
            uploaded_image.name.split('.')[-1])

        # validate and save image
        try:
            if uploaded_image.content_type not in MIME_WHITELIST:
                raise ValidationError('Image format invalid!')
            new_image = UploadedImage(image=uploaded_image)

            # apply model validations
            new_image.full_clean()
            new_image.save()

            # start processing image
            threading.Thread(target=process_uploaded_image, args=[new_image],
                daemon=True).start()
            # process_uploaded_image(new_image)

            res_body = {
                'progress_url': reverse('progress_url',
                    kwargs={'id': new_image.id}),
                'download_url': '{}{}.png'.format(settings.STATIC_URL, name)
            }
            return Response(res_body, status=status.HTTP_202_ACCEPTED)

        except ValidationError:
            res_body = {'error': 'Invalid image! Minimum accepted size is 200x200.'}
            return Response(res_body, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        ''' To list all the images that are not yet processed completely. '''

        images = UploadedImage.objects.filter(progress__lt=100)
        images = [{'name': image.image.name, 'progress': image.progress} \
            for image in images]
        return Response(images, status=status.HTTP_200_OK)


class Progress(APIView):
    ''' Interface to view progress of images. '''

    def get(self, request, id):
        try:
            image = UploadedImage.objects.get(pk=id)
            image = {'name': image.image.name, 'progress': image.progress}
            return Response(image, status=status.HTTP_200_OK)

        except UploadedImage.DoesNotExist:
            return Response({'error': 'Image does not exist!'},
                status=status.HTTP_404_NOT_FOUND)
