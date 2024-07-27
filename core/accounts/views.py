from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from time import sleep
from .tasks import sendEmail
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
# Create your views here.

def send_email(requset):
    sendEmail.delay()
    return HttpResponse("<h1>done sending mail</h1>")

@cache_page(60)
def test(request): 
    response = requests.get("https://6399c923-11f5-4080-ad3a-1d5dc57d910e.mock.pstmn.io/test/delay/5")
    return JsonResponse(response.json())

# def test(request):
#     if cache.get("test_delay_api") is None:
#         response = requests.get("https://6399c923-11f5-4080-ad3a-1d5dc57d910e.mock.pstmn.io/test/delay/5")
#         cache.set("test_delay_api", response.json())
    
#     return JsonResponse(cache.get("test_delay_api"))
