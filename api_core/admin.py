from django.contrib import admin
from api_core.models import *
# Register your models here.
# admin.site.register(About)
# admin.site.register(Packages)
class AboutCoverImageInline(admin.TabularInline):
    model = AboutCoverImage
    extra = 1  # Show 1 empty form by default
    fields = ('image', 'caption')  # Display only relevant fields

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutCoverImageInline]

    def delete_model(self, request, obj):
        for cover in obj.cover_images.all():
            cover.delete()  # call delete to remove image
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            for cover in obj.cover_images.all():
                cover.delete()
            obj.delete()

@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('disassembly_and_assembly', 'furniture_wrapping', 'packing_the_belongings')
    search_fields = ('mnames', )

'''
import os
from django.contrib import admin
from django.utils.html import format_html
from .models import About, AboutCoverImage, Packages

class AboutCoverImageInline(admin.TabularInline):
    model = AboutCoverImage
    extra = 1
    fields = ('image', 'caption', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return ""
    image_preview.short_description = "Preview"

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutCoverImageInline]
    list_display = ('name', 'created_at', 'updated_at')

    def delete_model(self, request, obj):
        # Delete cover images and logo
        for cover in obj.cover_images.all():
            cover.delete()
        if obj.logo and os.path.isfile(obj.logo.path):
            os.remove(obj.logo.path)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            for cover in obj.cover_images.all():
                cover.delete()
            if obj.logo and os.path.isfile(obj.logo.path):
                os.remove(obj.logo.path)
            obj.delete()

@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = (
        'disassembly_and_assembly',
        'furniture_wrapping',
        'packing_the_belongings',
        'wrapping_before_packing',
        'unpacking_and_organizing'
    )


'''