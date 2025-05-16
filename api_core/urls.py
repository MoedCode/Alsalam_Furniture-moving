#urls.py
from django.urls import path
from .views import *
from api_core.views_users import *
urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('logo/', AboutLogoView.as_view(), name='logo'),
    path('about/logo/', AboutLogoView.as_view(), name='about-logo'),
    path('about/form/', AboutFrom.as_view(), name='about_form'),
    path('packages/', PackagesView.as_view(), name='packages'),
    path('about/cover-image/', CoverImageServeView.as_view(), name='cover_image'),
    path('why-choose-us/', WhyChooseUsListView.as_view(), name='why-choose-us-list'),
    path('why-choose-us/image/', WhyChooseUsImageView.as_view(), name='whychooseus-image'),
    path('users/', UsersView.as_view(), name='user-view'),
    path('user/register/', UserRegister.as_view(), name='user/register'),
    path('register/', UserRegister.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/image/', ProfileImage.as_view(), name='profile_image'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('schema/', DynamicSchemaView.as_view(), name='dynamic-schema'),
]
