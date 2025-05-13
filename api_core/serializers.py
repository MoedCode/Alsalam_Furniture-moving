from rest_framework import serializers
from api_core.models import *


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = [
            "description",
            "who_we_are",
            "name",
            "logo",  # ← Ensure logo is included
        ]


class AboutCoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutCoverImage
        fields = ['id', 'image', 'caption']


class PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = [
            'name', 'price', 'disassembly_and_assembly',
            'furniture_wrapping', 'packing_the_belongings',
            'wrapping_before_packing', 'unpacking_and_organizing'
        ]
