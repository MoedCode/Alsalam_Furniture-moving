from api_core.views_H import *

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Disable CSRF check
class NoPostPermission(BasePermission):
    """
    Allow GET, PUT, DELETE only if authenticated.
    Deny POST completely.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False  # deny all POST
        # For others, require authentication
        return request.user and request.user.is_authenticated

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
    # permission_classes = [NoPostPermission]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
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

class ProfileView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    # permission_classes = [NoPostPermission]


    @extend_schema(responses=ProfileSerializer)
    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        profile, created = Profile.objects.get_or_create(user=request.user)
        status_ = S201 if created else S200
        serialized_prof = ProfileSerializer(profile)
        return Response(serialized_prof.data, status_)
    @extend_schema(request=ProfileSerializer, responses=ProfileSerializer)
    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        data = request.data.copy()
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']

        serializer = ProfileSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=S201)
        return Response(serializer.errors, status=S400)

    @extend_schema(request=ProfileSerializer, responses=ProfileSerializer)
    def put(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=S404)

        data = request.data.copy()
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']

        serializer = ProfileSerializer(profile, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=S200)
        return Response(serializer.errors, status=S400)

    def delete(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=S404)

        profile.delete()
        return Response(status=S204)
class ProfileImage(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=S401)

        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"detail": "User has no profile"}, status=S404)

        if not profile.image:
            return Response({"detail": "Profile has no image"}, status=S404)

        # Ensure the file exists on disk
        image_path = profile.image.path
        if not os.path.exists(image_path):
            return Response({"detail": "Image file not found on disk"}, status=S404)

        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')

