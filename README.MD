# 🚀 Blog API Platform

A production-style Blog API built with **FastAPI** following clean architecture principles.

The project is inspired by platforms like **Medium**, **Hashnode**, and **Dev.to**, focusing on scalable backend architecture, authentication, authorization, and modern API development.

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic
- Pydantic v2
- JWT Authentication
- Async SQLAlchemy
- Docker (Upcoming)
- Pytest (Upcoming)

---

## Features

### Authentication
- User Registration
- User Login
- JWT Access Token
- Refresh Token
- Logout
- Logout All Devices
- Current User Endpoint

### Authorization
- Role-Based Access Control (RBAC)
- USER
- AUTHOR
- ADMIN

### User Profile
- Public Profiles
- Update Profile
- Search Users
- Profile Information

---

## Project Structure

```
app/
│
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/
└── main.py
```

---

## Current Progress

- ✅ Project Setup
- ✅ Authentication
- ✅ JWT Authentication
- ✅ Refresh Tokens
- ✅ Authorization (RBAC)
- ✅ User Profile Module

### Upcoming

- Blog Posts
- Categories
- Tags
- Comments
- Likes
- Bookmarks
- Following System
- Notifications
- File Uploads
- Testing
- Docker
- CI/CD
- Deployment

---

## Run Locally

```bash
git clone https://github.com/Sk2059/BlogAPIPlatform.git

cd BlogAPIPlatform

python -m venv .venv

source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## License

This project is built for learning production-grade backend development using FastAPI.