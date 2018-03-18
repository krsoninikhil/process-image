from django.urls import path
from image_processing.views import ImageProcessing, Progress

urlpatterns = [
    path('', ImageProcessing.as_view(), name='process_image'),
    path('<id>', Progress.as_view(), name='progress_url'),
]
