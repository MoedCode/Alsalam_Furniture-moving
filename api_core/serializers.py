from rest_framework import serializers
from api_core.models import *

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        models = About
        fields = [
            "description,""who_we_are,""name,""logo,""cover_images,"
        ]