# users endpoints
## 1- create user
### request
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
```json
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
## 2- login user
### request

```json
{
  "username": "abdullah99",
  "password": "StrongPass123"
}
```

### response
```json
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Logged in successfully"
}
```
## 3- update user
### request

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
```json
HTTP 200 OK
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

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