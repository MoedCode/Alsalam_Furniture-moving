import os
import logging
from django.core.files.storage import default_storage
from rest_framework import status as S, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import FileResponse, Http404

from drf_spectacular.utils import extend_schema_view, extend_schema
logger = logging.getLogger(__name__)
from .models import *
from .serializers import *
S200 = S.HTTP_200_OK
S201 = S.HTTP_201_CREATED
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