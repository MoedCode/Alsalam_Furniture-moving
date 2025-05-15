
#models.py
from api_core.models_H import *

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

class Users(AbstractUser, Base):
    """
    Custom user for furniture‑moving site, with Saudi‑specific contact & location.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    password = models.CharField(
        max_length=128,
        help_text="Password (will be hashed automatically)"
    )
    phone_number = models.CharField(max_length=16, unique=True,
        help_text="Primary Saudi phone, e.g. +966501234567"
        )
    whatsapp_number = models.CharField(max_length=16, unique=True,
        help_text="Primary Saudi phone, e.g. +966501234567"
        )
    city  = models.CharField(
        max_length=100, help_text="City in Saudi Arabia"
        )
    postal_code = models.CharField(
        max_length=5, help_text="5‑digit Saudi postal code"
        )
    address = models.CharField(
        max_length=255,help_text="Street address / exact location"
        )
    def save(self, *args, **kwargs):
        if not self.is_superuser:
            # Validate phone numbers
            valid, msg = validate_phone(self.phone_number)
            if not valid:
                raise ValidationError({"phone_number": msg})

            valid, msg = validate_phone(self.whatsapp_number)
            if not valid:
                raise ValidationError({"whatsapp_number": msg})

            # Validate postal code and city
            valid, msg = validate_postal_city(self.postal_code, self.city)
            if not valid:
                raise ValidationError({"postal_code": msg})

        super().save(*args, **kwargs)
        is_new = self._state.adding
        if is_new:
            Profile.objects.create(user=self)


def profile_image_path(instance, filename):
    # Extension of uploaded file
    ext = filename.split('.')[-1]
    # Image saved as <profile_id>.<ext> in 'profile_images' folder
    return f'images/profile/{instance.id}.{ext}'

class Profile(Base):
    user = models.OneToOneField("Users", on_delete=models.CASCADE)  # Required link to User
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to=profile_image_path, blank=True, null=True)

    def delete_old_image(self):
        """Delete old image if it exists in 'profile_images' folder with profile id"""
        folder = 'profile_images'
        for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
            path = os.path.join(folder, f"{self.id}.{ext}")
            if os.path.isfile(path):
                os.remove(path)


    def save(self, *args, **kwargs):
        if self.id:  # Check if the object already has an ID (i.e., it's not a new object)
            try:
                old = Profile.objects.get(id=self.id)  # Try to fetch the existing object
                if old.image and old.image != self.image:  # Check if the image has changed
                    if os.path.isfile(old.image.path):  # If the old image exists, delete it
                        os.remove(old.image.path)
            except ObjectDoesNotExist:
                pass  # If the object doesn't exist (perhaps it was deleted), do nothing

        # Proceed with saving the object (whether it's a new one or an update)
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        # Delete image file when profile is deleted
        # self.delete_old_image()
        # super().delete(*args, **kwargs)
        if self.image and os.path.isfile(self.image.path):
            print(f"\n\n\n\n\n {self.image.path}")
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name or self.last_name else "Profile"
