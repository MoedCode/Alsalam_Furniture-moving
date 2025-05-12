from django.contrib import admin
from api_core.models import *
# Register your models here.
admin.site.register(About)
admin.site.register(Packages)
'''
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    # Show every concrete field in the changelist
    list_display = [f.name for f in About._meta.concrete_fields]
    # Allow filtering/searching if you like:
    search_fields = ['name', 'description', 'who_we_are']

@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Packages._meta.concrete_fields]
    list_filter = ['disassembly_and_assembly', 'packing_the_belongings']
    search_fields = ['name']
    '''