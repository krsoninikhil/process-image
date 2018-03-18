from django.db import models
from django.core.exceptions import ValidationError

import os
from PIL import Image

def check_dimensions(image):
    if image.height < 200 or image.width < 200:
        raise ValidationError('Image must be larger than 200x200 pixels!')


class UploadedImage(models.Model):
    ''' Representation of images in database. '''

    image = models.ImageField(upload_to='', validators=[check_dimensions])
    progress = models.PositiveIntegerField(default=0)


def process_uploaded_image(uploaded_image):
    ''' This is the actual processing of image. '''

    # get an PIL Image object
    image_pil = Image.open(uploaded_image.image)

    # converting to required 150x150 px
    image_pil.thumbnail((150, 150))

    # save in PNG format
    image_pil.save(os.path.join('media', 'processed_images',
        uploaded_image.image.name), 'PNG')

    # update the progress
    uploaded_image.progress = 100
    uploaded_image.save()
