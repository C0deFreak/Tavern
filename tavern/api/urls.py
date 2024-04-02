from django.urls import path
from .views import main

urlpatterns = [
    path('home', main) # Ide na ovu funkciju, sporedni url
]