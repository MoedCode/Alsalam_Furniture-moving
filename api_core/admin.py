from django.contrib import admin
from api_core.models import *
# Register your models here.
# admin.site.register(About)
# admin.site.register(Packages)
class AboutCoverImageInline(admin.TabularInline):
    model = AboutCoverImage
    extra = 1
    fields = ("image", "caption")
    verbose_name = "Cover Image"
    verbose_name_plural = "Cover Images"

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    fields = ("name", "description", "who_we_are", "logo")
    inlines = [AboutCoverImageInline]

@admin.register(AboutCoverImage)
class AboutCoverImageAdmin(admin.ModelAdmin):
    list_display = ("about", "image", "caption")
    list_filter  = ("about",)
