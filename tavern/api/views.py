from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# python manage.py runserver - pokreće server

def main(request):
    return HttpResponse("<h1>Hello<h1/>")