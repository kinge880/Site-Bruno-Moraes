from django.shortcuts import render
from django.http import HttpResponse

def landing_view(request):
    return render(request, 'public/landing.html')