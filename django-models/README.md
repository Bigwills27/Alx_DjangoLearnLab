# Django Models Relationships and Permissions Project

This Django project demonstrates the implementation of advanced ORM relationships, custom permissions, and role-based access control as specified in the ALX curriculum.

## Project Overview

This project is a duplicate of the `Introduction_to_Django` directory, renamed to `django-models` as per ALX Task 0 requirements. It includes a new app called `relationship_app` that showcases complex relationships between entities using ForeignKey, ManyToMany, and OneToOne fields.

## Project Structure

```
django-models/
└── LibraryProject/
    ├── manage.py
    ├── LibraryProject/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── relationship_app/
        ├── models.py          # Core models with relationships and permissions
        ├── views.py           # Function-based and class-based views
        ├── urls.py            # URL patterns
        ├── query_samples.py   # Sample ORM queries
        ├── admin.py           # Admin configuration
        └── templates/         # HTML templates
            └── relationship_app/
                ├── list_books.html
                ├── library_detail.html
                ├── login.html
                ├── logout.html
                ├── register.html
                ├── admin_view.html
                ├── librarian_view.html
                └── member_view.html
```

## Task 0: Advanced Model Relationships

### Models Implemented

1. **Author Model**
   - `name`: CharField
   - Demonstrates **one-to-many** relationship with Books

2. **Book Model**
   - `title`: CharField
   - `author`: ForeignKey to Author
   - **Meta class with custom permissions:**
     - `can_add_book`
     - `can_change_book`
     - `can_delete_book`

3. **Library Model**
   - `name`: CharField
   - `books`: ManyToManyField to Book
   - Demonstrates **many-to-many** relationship

4. **Librarian Model**
   - `name`: CharField
   - `library`: OneToOneField to Library
   - Demonstrates **one-to-one** relationship

5. **UserProfile Model**
   - `user`: OneToOneField to Django User
   - `role`: CharField with choices (Admin, Librarian, Member)
   - Auto-created via Django signals

### Relationship Types Demonstrated

- **ForeignKey**: Book → Author (one-to-many)
- **ManyToManyField**: Library ↔ Books (many-to-many)
- **OneToOneField**: Librarian → Library, UserProfile → User (one-to-one)

### Sample Queries (query_samples.py)

The `query_samples.py` file contains sample queries for each relationship:
- Query all books by a specific author
- List all books in a library
- Retrieve the librarian for a library

## Task 1: Django Views and URL Configuration

### Views Implemented

1. **Function-based View**
   - `list_books`: Lists all books with authors
   - Template: `list_books.html`

2. **Class-based View**
   - `LibraryDetailView`: DetailView showing library details
   - Template: `library_detail.html`

### URL Patterns

All views are accessible through configured URL patterns in `relationship_app/urls.py`.

## Task 2: User Authentication

### Authentication Features

- User registration with automatic UserProfile creation
- Login functionality using Django's built-in views
- Logout functionality
- Session management

### Templates

- `login.html`: User login form
- `logout.html`: Logout confirmation
- `register.html`: User registration form

## Task 3: Role-Based Access Control

### User Roles

- **Admin**: Full system access
- **Librarian**: Library management access
- **Member**: Basic user access

### Role-Based Views

- `admin_view`: Admin role only (uses `@user_passes_test`)
- `librarian_view`: Librarian role only
- `member_view`: Member role only

Each view checks the user's role before granting access.

## Task 4: Custom Permissions

### Custom Permissions in Book Model

```python
class Meta:
    permissions = [
        ('can_add_book', 'Can add book'),
        ('can_change_book', 'Can change book'),
        ('can_delete_book', 'Can delete book'),
    ]
```

### Permission-Protected Views

Views secured using Django's `@permission_required` decorator:
- `can_add_book_view`: Requires `can_add_book` permission
- `can_change_book_view`: Requires `can_change_book` permission
- `can_delete_book_view`: Requires `can_delete_book` permission

### URL Configuration

All secured views are accessible through specific URL patterns:
- `/add_book/`: Add book permission required
- `/edit_book/`: Change book permission required
- `/can_delete_book_view/`: Delete book permission required

## Setup and Usage

1. **Apply Migrations**:
   ```bash
   cd django-models/LibraryProject
   python manage.py makemigrations relationship_app
   python manage.py migrate
   ```

2. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the Application**:
   - Navigate to `http://127.0.0.1:8000/relationship_app/` for main views
   - Use admin interface to manage users and permissions

## Features Implemented

✅ **Advanced Model Relationships**: ForeignKey, ManyToMany, OneToOne
✅ **Function-based and Class-based Views**
✅ **User Authentication System**: Login, Logout, Registration
✅ **Role-based Access Control**: Admin, Librarian, Member roles
✅ **Custom Permissions**: Book model permissions
✅ **Permission-protected Views**: Using decorators
✅ **Proper URL Configuration**: All views properly routed
✅ **HTML Templates**: Complete template structure
✅ **Database Migrations**: All models migrated
✅ **Sample Queries**: ORM relationship demonstrations

This implementation satisfies all ALX requirements for Tasks 0-4 in the Django models curriculum.