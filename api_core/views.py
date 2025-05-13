from django.shortcuts import render

from api_core.views_H import *


class IsAdminAndLogged(permissions.BasePermission):
    """
    Allows access only to authenticated admin (staff) users.
    """
    def loggedAndPermission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.is_staff
            )

                # About Endpoints
class AboutView(APIView):
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
            # check if jusr admin who can update delete about images
    permission_classes = [IsAdminAndLogged]
    def post(self, request):
        """
        Creates or updates the single About instance.
        If an About exists, it performs a partial update; otherwise, it creates a new one.
        """
        about = about.object.first()
        if about:
            serialized = AboutSerializer(about, data=request.data, partial=True)
        else:
            serialized = AboutSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, S201)
        else:
            return Response(serialized.errors, S400)
    def put(self, request):
        """
        Updates the About section data (full update).
        Only accessible by admin users.
        """
        about = About.objects.filter()
        if not about:
            return Response({"detail": "About section does not exist."},S404)

        if 'logo' in request.data:
            if about.logo:
                try:
                    prev_path = about.logo.path
                    if os.path.exist(prev_path):
                        default_storage.delete(prev_path)
                except Exception as e:
                        logger.error(f"Failed to delete old logo image: {str(e)}", exc_info=True)
                serialized_about = AboutSerializer(about, data=request.data, partial=True)
                if serialized_about.is_valid():
                    serialized_about.save()
                    return Response(serialized_about.data, S200)
                else:
                    return Response(serialized_about.errors, S400)





class AboutFrom(APIView):
    permission_classes = [IsAdminAndLogged]
    def get(self, request):
        return render(request, "set_about.html")
class PackagesView(APIView):
    def get(self, request):
        packages = Packages.objects.all()
        if not packages:
            return Response({"detail":"About Packages Created yet"},S404)
        serialized_packages = PackagesSerializer(packages, many=True).data
        return Response({serialized_packages, S200})

    def post(self, request):
        serialized_package = PackagesSerializer(data=request.data)
        if not serialized_package or not serialized_package.is_valid:
            return Response(serialized_package.errors, S400)
        serialized_package.save()
        return Response(serialized_package.data, S201)
    def put(self, request):
        Package_id = request.query_params.get('id')
        if not Package_id:
            return Response({"details":"package"}, S404)
        try:
            package = Packages.objects.get(Package_id)
        except Packages.DoesNotExist:
            return Response({"detail":f"package {Package_id} not found"}, S404)
        serialized_package = PackagesSerializer(package, data=request.data, partial=True)
        if not serialized_package.is_valid():
            return Response(serialized_package.errors, S400)
        serialized_package.save()
        return Response(serialized_package.data, S200)
    def delete(self, request):
        Package_id = request.query_params.get('id')
        if not Package_id:
            return Response({"details":"package"}, S404)
        try:
            package = Packages.objects.get(Package_id)
        except Packages.DoesNotExist:
            return Response({"detail":f"package {Package_id} not found"}, S404)
        serialized_package = PackagesSerializer(package, data=request.data, partial=True)
        package.delete()
        return Response({"detail": f"Package {Package_id}deleted successfully"}, S200)
