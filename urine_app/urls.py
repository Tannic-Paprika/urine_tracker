from django.urls import path
from .views import upload_image, process_image

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('process_image/<path:image_url>/', process_image, name='process_image'),
]
