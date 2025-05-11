from django.shortcuts import render

from .views_main import *


class IsAdminAndLogged(permissions.BasePermission):
    """
    Allows access only to authenticated admin (staff) users.
    """
    def loggedAndPermission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.is_staff
            )
class SetAbout(APIView):
    """
    API endpoint to create or retrieve About section data.
    Only accessible to logged-in admin users.
    """
    def get(self, request):
        about = About.objects.first()
        if not about:
            return Response({"detail":"About Not Created yet"},S404)
        serialized = AboutSerializer(about).data
        return  Response(serialized, S200)
    permission_classes = [IsAdminAndLogged]
