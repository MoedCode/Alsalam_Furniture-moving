````markdown
# users endpoints

## 1 — Create User
### request
```http
POST /users/
Content-Type: application/json
````

```json
{
  "username": "abdullah99",
  "password": "StrongPass123",
  "email": "abdullah@example.com",
  "phone_number": "+966501234567",
  "whatsapp_number": "+966501234567",
  "city": "Riyadh",
  "postal_code": "11564",
  "address": "Olaya Street, Riyadh"
}
```

### response

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": "49aeb016-9039-4a9a-891f-e9266ed455fa",
    "username": "abdullah99",
    "phone_number": "+966501234567",
    "whatsapp_number": "+966501234567",
    "city": "Riyadh",
    "postal_code": "11564",
    "address": "Olaya Street, Riyadh",
    "first_name": "",
    "last_name": "",
    "email": "abdullah@example.com",
    "is_staff": false,
    "is_superuser": false,
    "is_active": true
}
```

---

## 2 — Login User

### request

```http
POST /login/
Content-Type: application/json
```

```json
{
  "username": "abdullah99",
  "password": "StrongPass123"
}
```

### response

```http
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Type: application/json

{
    "detail": "Logged in successfully"
}
```

---

## 3 — Update User

> *Must be authenticated*

### request

```http
PUT /users/
Content-Type: application/json
Authorization: Session / Cookie
```

```json
{
  "username": "abdullah99",
  "password": "StrongPass123",
  "email": "abdullah-alzoz@example.com",
  "phone_number": "+966501234567",
  "whatsapp_number": "+966501234567",
  "city": "Riyadh",
  "postal_code": "11564",
  "address": "Olaya Street, Riyadh"
}
```

### response

```http
HTTP/1.1 200 OK
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json

{
    "id": "49aeb016-9039-4a9a-891f-e9266ed455fa",
    "username": "abdullah99",
    "phone_number": "+966501234567",
    "whatsapp_number": "+966501234567",
    "city": "Riyadh",
    "postal_code": "11564",
    "address": "Olaya Street, Riyadh",
    "first_name": "",
    "last_name": "",
    "email": "abdullah-alzoz@example.com",
    "is_staff": false,
    "is_superuser": false,
    "is_active": true
}
```

---

# profile endpoints

## 1 — Get Profile

> *Must be authenticated*

### request

```http
GET /profile/
Authorization: Session / Cookie
```

### response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "69ec4d28-b92d-4343-a22a-723f5381e07a",
    "first_name": null,
    "last_name": null,
    "email": null,
    "image": "/media/images/profile/69ec4d28-b92d-4343-a22a-723f5381e07a.jpg"
}
```

---

## 2 — Create Profile

> *Must be authenticated*

### request

```http
POST /profile/
Content-Type: multipart/form-data
Authorization: Session / Cookie
```

*Form-data fields:*

* `first_name`: Abdullah
* `last_name`: Alzoz
* `email`: [abdullah99@example.com](mailto:abdullah99@example.com)
* `image`: (file)

### response

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": "69ec4d28-b92d-4343-a22a-723f5381e07a",
    "first_name": "Abdullah",
    "last_name": "Alzoz",
    "email": "abdullah99@example.com",
    "image": "/media/images/profile/69ec4d28-b92d-4343-a22a-723f5381e07a.jpg"
}
```

---

## 3 — Update Profile

> *Must be authenticated*

### request

```http
PUT /profile/
Content-Type: multipart/form-data
Authorization: Session / Cookie
```

*Form-data fields (any subset):*

* `first_name`: Abdullah Updated
* `email`: [abdullah-updated@example.com](mailto:abdullah-updated@example.com)
* `image`: (file) (optional)

### response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "69ec4d28-b92d-4343-a22a-723f5381e07a",
    "first_name": "Abdullah Updated",
    "last_name": "Alzoz",
    "email": "abdullah-updated@example.com",
    "image": "/media/images/profile/69ec4d28-b92d-4343-a22a-723f5381e07a.jpg"
}
```

---

## 4 — Delete Profile

> *Must be authenticated*

### request

```http
DELETE /profile/
Authorization: Session / Cookie
```

### response

```http
HTTP/1.1 204 No Content
```

---

## 5 — Get Profile Image

> *Must be authenticated*

### request

```http
GET /profile/image/
Authorization: Session / Cookie
```

### response (when exists)

```http
HTTP/1.1 200 OK
Content-Type: image/jpeg

(binary image data)
```

### response (when missing)

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
    "detail": "Profile has no image"
}
```

```
```

i wanna do Contacts class
which contain
1 - full name name should be in one field
2- phone number filed
    must be validated as saudi arabia phone number
3-email
4- catigory with optinal valuse just

5 -  message which will be text field
all fields in monitory
    1 -complaining
    2- Intelligence
    3- join us

also
FAQ class which simply qustion and answer
both are text fileds
```url
http://54.166.6.159/profile/
```
request body
```json
{
        "first_name": "mesh sho5lak",
    "last_name": "milzmaksh",
    "email": "nafs al kslam"
}
```
request file
```path
C:\Users\Active\Pictures\Camera Roll\FB_IMG_1684853676131.jpg
```
response body

```json
{
    "detail": "Unsupported media type \"image/jpeg\" in request."
}
```

endpoint/class/serializer
```py
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




```
