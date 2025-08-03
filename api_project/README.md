# Django REST Framework API Project

This project implements a complete RESTful API using Django REST Framework (DRF) following ALX specifications exactly.

## Project Structure

```
api_project/
├── manage.py
├── api_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── api/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── apps.py
    ├── tests.py
    ├── pop.py
    └── migrations/
```

## ALX Tasks Implementation

### Task 0: Setting Up Django Project with DRF ✅

**Objective**: Set up a new Django project with Django REST Framework

**Implementation**:
- ✅ Created Django project named `api_project`
- ✅ Installed Django REST Framework (`pip install djangorestframework`)
- ✅ Added `'rest_framework'` to `INSTALLED_APPS` in settings.py
- ✅ Created `api` app and added to `INSTALLED_APPS`
- ✅ Defined simple `Book` model with `title` and `author` fields (CharField)
- ✅ Created and applied migrations
- ✅ Server runs successfully on http://127.0.0.1:8000/

**Files Modified**:
- `api_project/settings.py`: Added DRF to INSTALLED_APPS
- `api/models.py`: Book model with title and author fields
- Database: SQLite with Book table

### Task 1: Building First API Endpoint ✅

**Objective**: Create a simple API endpoint to retrieve books using serializers and views

**Implementation**:
- ✅ Created `api/serializers.py` with `BookSerializer` extending `ModelSerializer`
- ✅ Includes all fields of Book model (`fields = '__all__'`)
- ✅ Created `BookList` view extending `rest_framework.generics.ListAPIView`
- ✅ Configured URL pattern: `path('books/', BookList.as_view(), name='book-list')`
- ✅ Main project URLs include `path('api/', include('api.urls'))`

**API Endpoint**:
- `GET /api/books/` - Lists all books (no authentication required)

**Files**:
- `api/serializers.py`: BookSerializer class
- `api/views.py`: BookList view
- `api/urls.py`: URL configuration
- `api_project/urls.py`: Main URL configuration

### Task 2: CRUD Operations with ViewSets and Routers ✅

**Objective**: Implement full CRUD operations using DRF ViewSets and Routers

**Implementation**:
- ✅ Created `BookViewSet` extending `rest_framework.viewsets.ModelViewSet`
- ✅ Provides all CRUD operations (list, create, retrieve, update, destroy)
- ✅ Used `DefaultRouter` and registered ViewSet as `books_all`
- ✅ URL pattern exactly as specified: `router.register(r'books_all', BookViewSet, basename='book_all')`
- ✅ URLs configured with both BookList and router URLs

**API Endpoints**:
- `GET /api/books_all/` - List all books
- `GET /api/books_all/<id>/` - Retrieve a book by ID
- `POST /api/books_all/` - Create a new book
- `PUT /api/books_all/<id>/` - Update a book
- `DELETE /api/books_all/<id>/` - Delete a book

**Files**:
- `api/views.py`: BookViewSet class
- `api/urls.py`: Router configuration

### Task 3: Authentication and Permissions ✅

**Objective**: Secure API endpoints with token authentication and permissions

**Implementation**:
- ✅ Added `'rest_framework.authtoken'` to `INSTALLED_APPS`
- ✅ Configured token authentication in `REST_FRAMEWORK` settings
- ✅ Added `DEFAULT_AUTHENTICATION_CLASSES` with TokenAuthentication
- ✅ Applied `IsAuthenticated` permission to BookViewSet
- ✅ Token retrieval endpoint using `obtain_auth_token`
- ✅ Migrations applied for token management

**Authentication Setup**:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**API Endpoints**:
- `POST /api/api-token-auth/` - Obtain authentication token

**Files**:
- `api_project/settings.py`: Authentication configuration
- `api/views.py`: Permission classes on ViewSet
- `api/urls.py`: Token authentication endpoint

## API Usage

### 1. Get Authentication Token

```bash
curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "adminpassword"}'
```

Response:
```json
{"token": "your-auth-token-here"}
```

### 2. List Books (No Authentication Required)

```bash
curl http://127.0.0.1:8000/api/books/
```

### 3. CRUD Operations (Authentication Required)

**List All Books:**
```bash
curl -H "Authorization: Token your-token" http://127.0.0.1:8000/api/books_all/
```

**Create Book:**
```bash
curl -X POST http://127.0.0.1:8000/api/books_all/ \
     -H "Authorization: Token your-token" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Book", "author": "New Author"}'
```

**Update Book:**
```bash
curl -X PUT http://127.0.0.1:8000/api/books_all/1/ \
     -H "Authorization: Token your-token" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Book", "author": "Updated Author"}'
```

**Delete Book:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/books_all/1/ \
     -H "Authorization: Token your-token"
```

## Testing

1. **Start the Server:**
   ```bash
   python manage.py runserver
   ```

2. **Run Test Script:**
   ```bash
   python test_api.py
   ```

3. **Manual Testing:**
   - Use Postman, curl, or browser to test endpoints
   - Test with and without authentication tokens
   - Verify CRUD operations work correctly

## Sample Data

The project includes sample users and books:

**Users:**
- admin/adminpassword
- john_doe/password123
- jane_smith/password123

**Books:**
- The Great Gatsby by F. Scott Fitzgerald
- To Kill a Mockingbird by Harper Lee
- 1984 by George Orwell
- Pride and Prejudice by Jane Austen
- The Catcher in the Rye by J.D. Salinger

## Security Features

- ✅ Token-based authentication
- ✅ Permission-based access control
- ✅ Secure ViewSet endpoints
- ✅ Proper HTTP methods handling
- ✅ JSON serialization/deserialization

## Compliance with ALX Requirements

This implementation strictly follows all ALX specifications:

1. **Project Structure**: Exactly as specified with `api_project` and `api` app
2. **Model Definition**: Simple Book model with title and author (CharField)
3. **URL Patterns**: Exact patterns as specified in instructions
4. **ViewSet Registration**: Router registered with `books_all` basename
5. **Authentication**: Token authentication as required
6. **Permissions**: IsAuthenticated for ViewSet operations
7. **Testing**: Comprehensive test coverage for all endpoints

## Next Steps

- Deploy to production environment
- Add more complex models and relationships
- Implement custom permissions
- Add API documentation with Swagger/OpenAPI
- Add rate limiting and throttling
- Implement pagination for large datasets
