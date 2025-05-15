import os
import re
import phonenumbers
# import geolocator
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import logging
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from django.db.models.signals import post_delete, pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser

logger = logging.getLogger("why_us")

class Base(models.Model):
    """
    Abstract base model with UUID primary key, creation and update timestamps,
    formatted and validated. Provides a to_dict method that excludes passwords
    and binary fields (e.g., FileField, ImageField).
    """
    time_format = '%d/%m/%Y/%H:%M:%S'
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="time. Format: DD/MM/YYYY/H:M:SS"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="time. Format: DD/MM/YYYY/H:M:SS"
    )

    class Meta:
        abstract = True

    def to_dict(self):
        """
        Return a dict representation of the model, formatting datetime fields
        as 'DD/MM/YYYY/H:M:SS' and excluding password and binary fields.
        """
        data = {}
        for filed in self._meta.concrete_fields:
            name = filed.name
            if 'password' in name.lower():
                continue
            if isinstance(filed, (models.FileField, models.ImageField)):
                continue
            value = getattr(self, name)
            if isinstance(filed, models.DateTimeField) and value is not None:
                value = value.strftime(self.__class__.time_format)
            data[name] = value
        return data

geolocator = Nominatim(user_agent="alsalam_furniture_app")

def validate_phone(value):
    """
    Check if number is a valid Saudi phone (e.g. +9665XXXXXXXX).
    Returns: (bool, message)
    """
    try:
        num = phonenumbers.parse(value, "SA")
    except phonenumbers.NumberParseException as e:
        return False, str(e)

    if not (phonenumbers.is_valid_number(num) and
            phonenumbers.region_code_for_number(num) == "SA"):
        return False, "Not a valid Saudi phone number."

    return True, "Valid Saudi phone number."

def validate_postal_city(postal_code, city):
    """
    Check if the postal code matches the city in Saudi Arabia.
    Returns: (bool, message)
    """
    try:
        location = geolocator.geocode({
            'postalcode': postal_code,
            'country': 'Saudi Arabia'
        }, language='en')
    except GeocoderServiceError:
        return False, "Unable to verify postal code at this time."

    if not location:
        return False, f"Postal code '{postal_code}' not found."

    address = location.address.lower()
    if city.lower() not in address:
        return False, f"Postal code '{postal_code}' does not match city '{city}'."

    return True, "City and postal code match."