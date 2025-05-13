from django.urls import path
from .views import *
urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('logo/', AboutLogoView.as_view(), name='logo'),
    path('about/form/', AboutFrom.as_view(), name='about_form'),
    path('packages/', PackagesView.as_view(), name='packages'),
    path('about/cover-image/', CoverImageServeView.as_view(), name='cover_image'),
]
