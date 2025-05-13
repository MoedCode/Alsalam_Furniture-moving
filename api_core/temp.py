import os
import logging
from django.core.files.storage import default_storage
from rest_framework import permissions, status as S
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api_core.models import About, AboutCoverImage
from api_core.serializers import AboutSerializer, AboutCoverImageSerializer

logger = logging.getLogger(__name__)


class IsAdminAndLogged(permissions.BasePermission):
    """
    Allows access only to authenticated admin (staff) users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class AboutView(APIView):
    """
    GET:    Retrieve About + logo URL + list of cover image URLs and captions.
    POST:   Create (or partial-update) About with logo + any number of cover images.
    PUT:    Full update of About + logo + cover images (old files cleaned up by model.save()).
    DELETE: Remove About + all cover images (files cleaned up by model.delete()).
    """
    permission_classes = [IsAdminAndLogged]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        about = About.objects.first()
        if not about:
            return Response({"detail": "About Not Created Yet"}, S.HTTP_404_NOT_FOUND)

        data = AboutSerializer(about).data
        # nest cover images
        covers = AboutCoverImage.objects.filter(about=about)
        data['cover_images'] = AboutCoverImageSerializer(
            covers, many=True).data
        return Response(data, S.HTTP_200_OK)

    def post(self, request):
        """
        Creates or updates the single About instance.
        If an About exists, it performs a partial update; otherwise, it creates a new one.
        """
        about = About.objects.first()
        serializer = AboutSerializer(
            about, data=request.data, partial=True) if about else AboutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, S.HTTP_400_BAD_REQUEST)

        about = serializer.save()  # About.save() cleans old logo
        # handle multiple new cover images
        files = request.FILES.getlist('cover_images')
        captions = request.data.getlist('captions', [])
        for idx, img in enumerate(files):
            cap = captions[idx] if idx < len(captions) else ''
            AboutCoverImage.objects.create(about=about, image=img, caption=cap)
        return Response(AboutSerializer(about).data, S.HTTP_201_CREATED)

    def put(self, request):
        about = About.objects.first()
        if not about:
            return Response({"detail": "About section does not exist."}, S.HTTP_404_NOT_FOUND)

        # full update
        serializer = AboutSerializer(about, data=request.data, partial=False)
        if not serializer.is_valid():
            return Response(serializer.errors, S.HTTP_400_BAD_REQUEST)

        about = serializer.save()  # About.save() deletes old logo file automatically

        # if new cover_images supplied, delete old ones:
        if 'cover_images' in request.FILES:
            for old in about.cover_images.all():
                old.delete()  # AboutCoverImage.delete() removes file
        # then create new ones
        files = request.FILES.getlist('cover_images')
        captions = request.data.getlist('captions', [])
        for idx, img in enumerate(files):
            cap = captions[idx] if idx < len(captions) else ''
            AboutCoverImage.objects.create(about=about, image=img, caption=cap)

        return Response(AboutSerializer(about).data, S.HTTP_200_OK)

    def delete(self, request):
        about = About.objects.first()
        if not about:
            return Response({"detail": "About section does not exist."}, S.HTTP_404_NOT_FOUND)
        about.delete()  # triggers About.delete() and AboutCoverImage.delete() to clean up files
        return Response(status=S.HTTP_204_NO_CONTENT)
