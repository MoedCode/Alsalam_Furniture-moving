# views.py
from django.shortcuts import get_object_or_404, render
from django.conf import settings
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
    GET:    Retrieve About + logo URL + list of cover image URLs and captions.
    POST:   Create (or partial-update) About with logo + any number of cover images.
    PUT:    Full update of About + logo + cover images (old files cleaned up by model.save()).
    DELETE: Remove About + all cover images (files cleaned up by model.delete()).
    """
    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def get(self, request):
        about = About.objects.first()
        if not about:
            return Response({"detail": "About Not Created yet"}, S404)
        about_data = AboutSerializer(about).data
        # git all about cover images
        covers = AboutCoverImage.objects.filter(about=about)
        # serialize them all result list of dictionaries
        about_data['cover_images'] = AboutCoverImageSerializer(
            covers, many=True).data
        return Response(about_data, S200)

    # check if jusr admin who can update delete about images
    permission_classes = [IsAdminAndLogged]

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def post(self, request):
        """
        Creates or updates the single About instance.
        If an About exists, it performs a partial update; otherwise, it creates a new one.
        """
        about = about.objects.first()
        if about:
            serialized = AboutSerializer(
                about, data=request.data, partial=True)
        else:
            serialized = AboutSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(serialized.errors, S400)

        serialized.save()
        # get and save cover images
        try:
            files = request.FILES.getlist('cover_images')
            captions = request.data.getlist('captions', [])
            for idx, imag in enumerate(files):
                cap = captions[idx] if idx < len(captions) else ''
                AboutCoverImage.objects.create(
                    about=about, imag=imag, caption=cap)
        except Exception as E:
            return Response({"detail": f"error saving cover images {str(E)}"}, S500)
        return Response(AboutSerializer(about).data, S201)

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def put(self, request):
        about = About.objects.first()
        if not about:
            return Response({"detail": "About section does not exist."}, S.HTTP_404_NOT_FOUND)

        # update About base fields and logo
        serializer = AboutSerializer(about, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, S.HTTP_400_BAD_REQUEST)
        about = serializer.save()  # About.save() handles logo cleanup

        # delete specific cover images by ID
        ids_to_delete = request.data.getlist('delete_cover_ids')
        for cover_id in ids_to_delete:
            try:
                cover = AboutCoverImage.objects.get(id=cover_id, about=about)
                cover.delete()  # calls AboutCoverImage.delete()
            except AboutCoverImage.DoesNotExist:
                logger.warning(
                    f"Cover image ID {cover_id} not found or doesn't belong to this About.")

        # add new cover images
        files = request.FILES.getlist('cover_images')
        captions = request.data.getlist('captions', [])
        for idx, img in enumerate(files):
            caption = captions[idx] if idx < len(captions) else ''
            AboutCoverImage.objects.create(
                about=about, image=img, caption=caption)

        return Response(AboutSerializer(about).data, S.HTTP_200_OK)

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def delete(self, request):
        about = About.objects.first()
        if not about:
            return Response({"detail": "About section does not exist."}, S.HTTP_404_NOT_FOUND)
        about.delete()  # triggers About.delete() and AboutCoverImage.delete() to clean up files
        return Response(status=S.HTTP_204_NO_CONTENT)


class CoverImageServeView(APIView):
    """
    Public endpoint to serve About cover images directly by ID or filename.
    Expects image_id or filename in request.data (POST).

    """
    permission_classes = []  # Public access

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def post(self, request):
        try:
            image_id = request.data.get('image_id')
            filename = request.data.get('filename')

            if image_id:
                cover = AboutCoverImage.objects.get(id=image_id)
                file_path = cover.image.path
            elif filename:
                file_path = os.path.join(
                    settings.MEDIA_ROOT, 'images/about/covers', filename)
            else:
                return Response({"detail": "image_id or filename must be provided."}, status=400)

            if not os.path.exists(file_path):
                raise FileNotFoundError

            return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')

        except AboutCoverImage.DoesNotExist:
            raise Http404("Image with this ID not found.")
        except FileNotFoundError:
            raise Http404("Image file not found.")
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

class AboutLogoView(APIView):
    """
    GET: Return the logo image file from the About section.
    """
    def get(self, request):
        about = About.objects.first()
        if not about or not about.logo:
            raise Http404("Logo not found.")

        return FileResponse(about.logo.open("rb"), content_type="image/*")


@extend_schema_view(
    get=extend_schema(exclude=True)
)
class AboutFrom(APIView):
    permission_classes = [IsAdminAndLogged]

    def get(self, request):
        return render(request, "set_about.html")


class PackagesView(APIView):
    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def get(self, request):
        packages = Packages.objects.all()
        if not packages:
            return Response({"detail": "About Packages Created yet"}, S404)
        serialized_packages = PackagesSerializer(packages, many=True).data
        return Response({serialized_packages, S200})

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def post(self, request):
        serialized_package = PackagesSerializer(data=request.data)
        if not serialized_package or not serialized_package.is_valid:
            return Response(serialized_package.errors, S400)
        serialized_package.save()
        return Response(serialized_package.data, S201)

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def put(self, request):
        Package_id = request.query_params.get('id')
        if not Package_id:
            return Response({"details": "package"}, S404)
        try:
            package = Packages.objects.get(Package_id)
        except Packages.DoesNotExist:
            return Response({"detail": f"package {Package_id} not found"}, S404)
        serialized_package = PackagesSerializer(
            package, data=request.data, partial=True)
        if not serialized_package.is_valid():
            return Response(serialized_package.errors, S400)
        serialized_package.save()
        return Response(serialized_package.data, S200)

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def delete(self, request):
        Package_id = request.query_params.get('id')
        if not Package_id:
            return Response({"details": "package"}, S404)
        try:
            package = Packages.objects.get(Package_id)
        except Packages.DoesNotExist:
            return Response({"detail": f"package {Package_id} not found"}, S404)
        serialized_package = PackagesSerializer(
            package, data=request.data, partial=True)
        package.delete()
        return Response({"detail": f"Package {Package_id}deleted successfully"}, S200)



class WhyChooseUsListView(APIView):
    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def get(self, request):
        queryset = WhyChooseUs.objects.all()
        serializer = WhyChooseUsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, S200)


class WhyChooseUsImageView(APIView):
    """
    Retrieve image of a WhyChooseUs instance by ID or image path.
    Supports ?id=<uuid> or ?image=<relative_path>
    """
    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def post(self, request):
        uuid = request.data.get("id")
        image_path = request.data.get("image")

        try:
            if uuid:
                obj = WhyChooseUs.objects.get(id=uuid)
                print(f"z\n\n\n{obj}\n\n\n")
                if obj.image:
                    return FileResponse(obj.image.open(), content_type='image/jpeg')

            elif image_path:
                from django.conf import settings
                abs_path = os.path.join(settings.MEDIA_ROOT, image_path)
                if os.path.exists(abs_path):
                    return FileResponse(open(abs_path, 'rb'), content_type='image/jpeg')
        except WhyChooseUs.DoesNotExist:
            raise Http404("Object not found")

        return Response({"detail": "Image not found"}, S404)
class  UserRegister(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=S400)

        try:
            serializer.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=S500)

        return Response(serializer.data, status=S201)
class UsersView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [NoPostPermission]
    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        serializer = UsersSerializer(request.user)
        return Response(serializer.data, status=S200)


    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=S400)

        try:
            serializer.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=S500)

        return Response(serializer.data, status=S201)

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def put(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        serializer = UsersSerializer(request.user, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=S400)

        try:
            serializer.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=S500)

        return Response(serializer.data, status=S200)

    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def delete(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        try:
            request.user.delete()
            return Response({"detail": "User deleted"}, status=S204)
        except Exception as e:
            return Response({"detail": str(e)}, status=S500)


class LoginView(APIView):
    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Logged in successfully'})
        return Response({'detail': 'Invalid credentials'}, S401)

class LogoutView(APIView):
    @extend_schema(request=PackagesSerializer, responses=PackagesSerializer)
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'})