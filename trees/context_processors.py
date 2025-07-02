from django.conf import settings

def base_image_url(request):
    return {
        'BASE_IMAGE_URL': settings.BASE_IMAGE_URL
    }
