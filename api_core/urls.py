from django.urls import path
from .views import *
urlpatterns = [
    path('about/', SetAbout.as_view(), name='about'),
    path('about/form', SetAboutFrom.as_view(), name='about_form'),
]