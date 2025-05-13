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
    list_filter = ('disassembly_and_assembly',
                   'furniture_wrapping', 'packing_the_belongings')
    search_fields = ('mnames', )



admin.site.register(WhyChooseUs)