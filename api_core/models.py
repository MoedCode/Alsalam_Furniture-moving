
#models.py
from api_core.models_H import *
from api_core.models_users import *
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
    paragraphs = models.JSONField(
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


    def save(self, *args, **kwargs):
        if self.id:  # Check if the object already has an ID (i.e., it's not a new object)
            try:
                old = WhyChooseUs.objects.get(id=self.id)  # Try to fetch the existing object
                if old.image and old.image != self.image:  # Check if the image has changed
                    if os.path.isfile(old.image.path):  # If the old image exists, delete it
                        os.remove(old.image.path)
            except ObjectDoesNotExist:
                pass  # If the object doesn't exist (perhaps it was deleted), do nothing

        # Proceed with saving the object (whether it's a new one or an update)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

        # Reorder after deletion
        for idx, item in enumerate(WhyChooseUs.objects.order_by('order')):
            if item.order != idx:
                item.order = idx
                item.save(update_fields=['order'])
    def clean(self):
        if not isinstance(self.paragraphs, list) or not self.paragraphs:
            raise ValidationError({"paragraphs": "At least one paragraph is required."})

        for p in self.paragraphs:
            if not p.strip():
                raise ValidationError({"paragraphs": "Empty paragraphs are not allowed."})

