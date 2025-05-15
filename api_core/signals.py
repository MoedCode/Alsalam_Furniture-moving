#signals.py

import os
import logging
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from api_core.models import About, AboutCoverImage  # avoid wildcard imports

logger = logging.getLogger(__name__)  # Use module-level logger


def delete_file(file_field):
    try:
        if file_field and hasattr(file_field, 'path') and os.path.isfile(file_field.path):
            os.remove(file_field.path)
    except Exception as e:
        logger.error(f"[Image Deletion Error] {str(e)}", exc_info=True)

# --- About Logo ---


@receiver(pre_save, sender=About)
def delete_logo_on_update(sender, instance, **kwargs):
    if not instance.id:
        return  # new object, nothing to compare
    try:
        prev = About.objects.get(id=instance.id)
    except About.DoesNotExist:
        return
    if prev.logo and prev.logo != instance.logo:
        delete_file(prev.logo)


@receiver(post_delete, sender=About)
def delete_logo_on_delete(sender, instance, **kwargs):
    delete_file(instance.logo)

# --- Cover Images ---


@receiver(pre_save, sender=AboutCoverImage)
def delete_cover_on_update(sender, instance, **kwargs):
    if not instance.id:
        return  # new object
    try:
        prev = AboutCoverImage.objects.get(id=instance.id)
    except AboutCoverImage.DoesNotExist:
        return
    if prev.image and prev.image != instance.image:
        delete_file(prev.image)


@receiver(post_delete, sender=AboutCoverImage)
def delete_cover_on_delete(sender, instance, **kwargs):
    delete_file(instance.image)
