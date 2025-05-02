from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.

def user_logout(request):
    logout(request)
    return HttpResponse("logout page")

def profile(request):
    return HttpResponse("profile page")