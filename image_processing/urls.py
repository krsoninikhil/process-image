from django.urls import path
from image_processing.views import ImageProcessing, ProcessedImage

urlpatterns = [
    path('', ImageProcessing.as_view(), name='process_image'),
    path('<name>', ProcessedImage.as_view(), name='processed_image'),
]
