#  Template CRUD Service


- **Flask** for the backend framework.
- **MongoDB** for data storage.
- **JWT (JSON Web Token)** for authentication.
- **Bcrypt** for password hashing.

## Project Structure

- `app.py` - The main application file with routes and logic.
- `rsa_privkey.json` - Private key for JWT.
- `requirements.txt` - Python dependencies.

## Hosted Service

The service is hosted and accessible via the following link:

[Flask CRUD Hosted Service](https://flask-crud-template.onrender.com)

## Endpoints


### 1. **User Registration**

**Endpoint:** `POST /register`

```bash
curl -X POST https://flask-crud-jbel.onrender.com/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Pooja",
    "last_name": "Shree",
    "email": "poojashree@spiceblue.com",
    "password": "pooja@135"
  }'
```

---

### 2. **User Login**

**Endpoint:** `POST /login`

```bash
curl -X POST https://flask-crud-jbel.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "poojashree@spiceblue.com",
    "password": "pooja@135"
  }'
```

- **Response:** This will return a JWT token that you will use in the following requests.

---

### 3. **Create Template**

**Endpoint:** `POST /template`

**Requires Authorization (JWT token in headers)**

```bash
curl -X POST https://flask-crud-jbel.onrender.com/template \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "template_name": "New Template",
    "subject": "New Subject",
    "body": "New body text."
  }'
```

Replace `<JWT_TOKEN>` with the token received from the `/login` endpoint. This will return the `ID` of the created template.

---

### 4. **Get All Templates**

**Endpoint:** `GET /template`

**Requires Authorization (JWT token in headers)**

```bash
curl -X GET https://flask-crud-jbel.onrender.com/template \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

---

### 5. **Get Single Template**

**Endpoint:** `GET /template/<template_id>`

**Requires Authorization (JWT token in headers)**

```bash
curl -X GET https://flask-crud-jbel.onrender.com/template/<template_id> \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

Replace `<template_id>` with the ID of the template you want to retrieve.

---

### 6. **Update Template**

**Endpoint:** `PUT /template/<template_id>`

**Requires Authorization (JWT token in headers)**

```bash
curl -X PUT https://flask-crud-jbel.onrender.com/template/<template_id> \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "template_name": "Updated Template",
    "subject": "Updated Subject",
    "body": "Updated body text."
  }'
```

Replace `<template_id>` with the ID of the template you want to update.

---

### 7. **Delete Template**

**Endpoint:** `DELETE /template/<template_id>`

**Requires Authorization (JWT token in headers)**

```bash
curl -X DELETE https://flask-crud-jbel.onrender.com/template/<template_id> \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

Replace `<template_id>` with the ID of the template you want to delete.

---
