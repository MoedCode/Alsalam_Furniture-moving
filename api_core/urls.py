from django.urls import path
from .views import *
urlpatterns = [
    path('about/', SetAbout.as_view(), name='about')
]