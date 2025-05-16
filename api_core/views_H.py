#views_H.py
from .serializers import *
import os
import logging
from django.core.files.storage import default_storage
from rest_framework import status as S, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import FileResponse, Http404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from drf_spectacular.utils import extend_schema_view, extend_schema
logger = logging.getLogger(__name__)
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from api_core.models import (
    About, WhyChooseUs,  Packages, AboutCoverImage,
    Users, Profile
    )

S200 = S.HTTP_200_OK
S201 = S.HTTP_201_CREATED
S202 = S.HTTP_202_ACCEPTED
S203 = S.HTTP_203_NON_AUTHORITATIVE_INFORMATION
S204 = S.HTTP_204_NO_CONTENT
S205 = S.HTTP_205_RESET_CONTENT
S304 = S.HTTP_304_NOT_MODIFIED
S400 = S.HTTP_400_BAD_REQUEST
S401 = S.HTTP_401_UNAUTHORIZED
S405 = S.HTTP_405_METHOD_NOT_ALLOWED
S403 = S.HTTP_403_FORBIDDEN
S404 = S.HTTP_404_NOT_FOUND
S405 = S.HTTP_405_METHOD_NOT_ALLOWED
S406 = S.HTTP_406_NOT_ACCEPTABLE
S408 = S.HTTP_408_REQUEST_TIMEOUT
S500 = S.HTTP_500_INTERNAL_SERVER_ERROR
class DynamicSchemaView(APIView):
    """
    API endpoint that generates and returns the OpenAPI schema JSON on-demand.
    """

    @extend_schema(
        description="Get the current OpenAPI JSON schema",
        responses={200: dict},
    )
    def get(self, request, *args, **kwargs):
        generator = SchemaGenerator(title="Your API Title")
        schema = generator.get_schema(request=request)
        return Response(schema)