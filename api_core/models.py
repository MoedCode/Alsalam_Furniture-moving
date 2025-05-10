from  uuid import uuid4
from django.db import models
from django.utils import timezone
from django.db import models

# Create your models here.
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
        auto_now_add = True, help_text="time. Format: DD/MM/YYYY/H:M:SS"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="time. Format: DD/MM/YYYY/H:M:SS"
    )
    class Meta:
        abstract =True
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


class About(Base):
    """
    Represents the 'About' section of the website, with required logo and optional image.
    """
    description = models.TextField(
    help_text="General description about the company or service."
    )
    who_we_are = models.TextField(
    help_text="Detailed description of who you are as a company."
    )
    name = models.CharField(
    max_length=255,
    help_text="Company or website name."
    )
    logo = models.ImageField(
    upload_to='images/logos',
    null=False,
    blank=False,
    help_text="Required company logo."
    )
    cover_images = models.ImageField(
    upload_to='images/about',
    null=True,
    blank=True,
    help_text="Optional additional image."
    )
class Meta:
    verbose_name = "About"
    verbose_name_plural = "About Section"
    ordering = ["created"]

def __str__(self):
    return f"{self.name}"
class Packages(Base):
    """
    Stores package offerings mirroring the lockers.sa structure:
    - name: Package name (Economic, Economic+, Basic, Comprehensive)
    - price: Price per trip (SAR)
    - boolean flags for included services
    """
    name = models.CharField(
        max_length=50, unique=True, help_text="Package name",
        null=False
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Amount of The Trip"
    )
    disassembly_and_assembly = models.BooleanField(
        default=True,
        help_text="Disassembly and Assembly included"
    )
    furniture_wrapping = models.BooleanField(
        default=True,
        help_text="Unlimited Cardboards (Boxes) included"
    )
    packing_the_belongings = models.BooleanField(
        default=True,
        help_text="Packing the Belongings included"
    )
    wrapping_before_packing = models.BooleanField(
        default=True,
        help_text="Wrapping before Packing included"
    )
    unpacking_and_organizing = models.BooleanField(
        default=True,
        help_text="Unpacking and organizing in your new house included"
    )
    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} – {self.price} SAR"