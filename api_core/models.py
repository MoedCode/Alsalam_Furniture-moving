import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import logging

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


class About(Base):
    """
    Represents the 'About' section of the website, with required logo.
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
        blank=False,
        help_text="Required company logo."
    )

    def __str__(self):
        return self.name

    class Meta:                       # ← indented under About
        verbose_name = "About"
        verbose_name_plural = "About Section"

    def save(self, *args, **kwargs):
        try:
            old = About.objects.get(id=self.id)
            if old.logo and old.logo != self.logo:
                if os.path.isfile(old.logo.path):
                    os.remove(old.logo.path)
        except About.DoesNotExist:
            pass  # New object, no old image to remove
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.logo and os.path.isfile(self.logo.path):
            os.remove(self.logo.path)
        super().delete(*args, **kwargs)


class AboutCoverImage(Base):
    """
    Stores multiple cover images (with optional caption) for the About section.
    """
    about = models.ForeignKey(
        'About',
        on_delete=models.CASCADE,
        related_name='cover_images',
        help_text="The About section this image is linked to."
    )
    image = models.ImageField(
        upload_to='images/about/covers',
        help_text="Promotional cover image."
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional text shown below the image."
    )

    def __str__(self):
        return f"Cover image for {self.about.name}"

    class Meta:                       # ← indented under CoverImage
        verbose_name = "about Cover Image"
        verbose_name_plural = "Cover Images"

    def save(self, *args, **kwargs):
        try:
            old = AboutCoverImage.objects.get(id=self.id)
            if old.image and old.image != self.image:
                if os.path.isfile(old.image.path):
                    os.remove(old.image.path)
        except AboutCoverImage.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


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

class WhyChooseUs(Base):
    """
    Represents a "Why Choose Us" item with an image, paragraphs, and a strict display order.

    Fields:
    - image: Optional image displayed above the text.
    - paragraphs: List of 1 or more explanatory paragraphs.
    - order: Unique integer (0-based or 1-based) to control front-end display order.

    Features:
    - Old image is deleted on update/delete.
    - Enforces gapless order.
    """
    image = models.ImageField(
        upload_to="images/why_us",
        blank=True, null=True,
        help_text="Optional illustrative image."
    )
    paragraphs = ArrayField(
        models.TextField(),
        blank=False,
        default=list,
        help_text="List of paragraphs (at least one required)."
    )
    order = models.PositiveIntegerField(
        unique=True,
        help_text="Display order. Must be unique and gap-free (starts at 0)."
    )

    class Meta:
        verbose_name = "Why Choose Us Item"
        verbose_name_plural = "Why Choose Us Items"
        ordering = ["order"]

    def __str__(self):
        return f"Why Choose Us #{self.order}"

    def clean(self):
        """
        Validation:
        - Must include at least one paragraph.
        """
        if not self.paragraphs or not isinstance(self.paragraphs, list):
            raise ValidationError("At least one paragraph is required.")


@receiver(pre_save, sender=WhyChooseUs)
def delete_old_image_on_update(sender, instance, **kwargs):
    """
    If the image is changed, delete the old file from disk.
    """
    if not instance.pk:
        return
    try:
        old = WhyChooseUs.objects.get(pk=instance.pk)
        if old.image and old.image != instance.image:
            if os.path.isfile(old.image.path):
                os.remove(old.image.path)
                logger.info(f"Old image deleted: {old.image.path}")
    except WhyChooseUs.DoesNotExist:
        pass


@receiver(post_delete, sender=WhyChooseUs)
def delete_image_and_reorder(sender, instance, **kwargs):
    """
    Deletes the image file and reorders remaining items to ensure gap-free order.
    """
    # Delete image
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
        logger.info(f"Image deleted: {instance.image.path}")

    # Reorder remaining
    items = WhyChooseUs.objects.order_by("order")
    for index, item in enumerate(items):
        if item.order != index:
            item.order = index
            item.save(update_fields=["order"])