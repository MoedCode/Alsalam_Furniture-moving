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


from rest_framework import serializers
from .models import WhyChooseUs

class WhyChooseUsSerializer(serializers.ModelSerializer):


    class Meta:
        model = WhyChooseUs
        fields = ['id', 'image', 'paragraphs', 'order']



    def validate_paragraphs(self, value):
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError("At least one paragraph is required.")
        for paragraph in value:
            if not paragraph.strip():
                raise serializers.ValidationError("Empty paragraphs are not allowed.")
        return value

