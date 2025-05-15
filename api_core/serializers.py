#serializers.py

from rest_framework import serializers
from api_core.models import *
from django.contrib.auth.hashers import make_password

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

class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = Users
        fields = [
            'id','username','password','phone_number','whatsapp_number',
            'city','postal_code','address','first_name','last_name','email','is_staff','is_superuser','is_active',
        ]
        read_only_fields = [
            'is_staff', 'is_superuser', 'is_active', 'id'
            # 'created_at', 'undated_at'
        ]

    def validate_phone_number(self, value):
        valid, msg = validate_phone(value)
        if not valid:
            raise serializers.ValidationError(msg)
        return value

    def validate_whatsapp_number(self, value):
        valid, msg = validate_phone(value)
        if not valid:
            raise serializers.ValidationError(msg)
        return value

    def validate(self, data):
        postal_code = data.get('postal_code', None)
        city = data.get('city', None)

        if postal_code and city:
            valid, msg = validate_postal_city(postal_code, city)
            if not valid:
                raise serializers.ValidationError({'postal_code': msg})

        return data

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Hash password if it's updated
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'email', 'image']
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
            'image': {'required': False, 'allow_null': True},
        }

    def validate_email(self, value):
        if value and '@' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value