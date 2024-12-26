from django.test import TestCase

# Create your tests here.

def get_user_ip(request):
    get_ip = request.META.get('HTTP_X_FORWARDED_FOR')

    if get_ip:
        ip = get_ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip