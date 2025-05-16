from api_core.models_H import *
from django.core.validators import RegexValidator, EmailValidator


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

def Contacts(Base):
    CATEGORY_CHOICES = [
        ('complaining', 'Complaining', "شكوي"),
        ('intelligence', 'Intelligence', "استخبار"),
        ('join_us', 'Join Us', ""),
    ]
    full_name = models.CharField(max_length=255)
    phonenumbers = models.CharField(max_length=16, unique=False,
        help_text="Saudi phone number, e.g. +966501234567",
        blank=False,
    )
    email = models.CharField(
        help_text="Contact email address.",
        blank=False,
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES,
        help_text="Type of message.",
    )