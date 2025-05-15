#admin.py

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


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('order', '__str__')
    ordering = ('order',)

    def delete_model(self, request, obj):
        obj.delete()  # This triggers the custom delete method in the model

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()  # Ensure batch deletes also call the custom method
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):

    # Fields to display in the user list view in admin panel
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Fields you can filter users by in the sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Fields used in search box
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Fields to order the list by
    ordering = ('username',)

    # The fieldsets control the layout of the user edit form in the admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ( 'phone_number', 'whatsapp_number', 'city', 'postal_code', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields that appear when creating a new user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Password validation fields to make create user form work with hashed passwords
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['password'].help_text = (
            "Raw passwords are not stored, so you cannot see the password."
        )
        return form
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'image')
    search_fields = ('first_name', 'last_name', 'email')
    def delete_model(self, request, obj):
        obj.delete()  # This triggers the custom delete method in the model

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()