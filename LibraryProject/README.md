# Django Models Relationships and Permissions Project

This Django project demonstrates the implementation of advanced ORM relationships, custom permissions, and role-based access control.

## Project Structure

```
LibraryProject/
├── manage.py
├── LibraryProject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── relationship_app/
    ├── models.py          # Contains all model definitions with relationships
    ├── views.py           # Contains views with permission decorators
    ├── urls.py            # URL patterns for all views
    ├── admin.py           # Admin interface configuration
    └── templates/         # HTML templates for views
```

## Models Implemented

### Core Models with Relationships

1. **Author Model**
   - Simple model with name field
   - One-to-many relationship with Books

2. **Book Model** 
   - Title and author fields
   - ForeignKey relationship to Author
   - **Custom Meta class with permissions:**
     - `can_add_book`
     - `can_change_book` 
     - `can_delete_book`

3. **Library Model**
   - Name field
   - ManyToMany relationship with Books

4. **Librarian Model**
   - Name field
   - OneToOne relationship with Library

5. **UserProfile Model**
   - OneToOne relationship with Django User
   - Role choices: Admin, Librarian, Member
   - Auto-created via Django signals

## Relationship Types Demonstrated

- **ForeignKey**: Book → Author (one-to-many)
- **ManyToMany**: Library ↔ Books (many-to-many)  
- **OneToOne**: Librarian → Library, UserProfile → User (one-to-one)

## Permission System

### Custom Permissions in Book Model
The Book model includes a nested Meta class with custom permissions:

```python
class Meta:
    permissions = [
        ('can_add_book', 'Can add book'),
        ('can_change_book', 'Can change book'),
        ('can_delete_book', 'Can delete book'),
    ]
```

### Permission-Protected Views
Views are secured using Django's `@permission_required` decorator:

- `can_add_book_view` - Requires `can_add_book` permission
- `can_change_book_view` - Requires `can_change_book` permission  
- `can_delete_book_view` - Requires `can_delete_book` permission

## Role-Based Access Control

### User Roles
- **Admin**: Full system access
- **Librarian**: Library management access
- **Member**: Basic user access

### Role-Based Views
- `admin_view` - Admin role only
- `librarian_view` - Librarian role only
- `member_view` - Member role only

## Authentication System

- User registration with automatic UserProfile creation
- Login/logout functionality
- Role assignment and verification
- Permission-based access control

## URLs Configuration

All views are accessible through properly configured URL patterns in `relationship_app/urls.py`:

- `/add_book/` - Add book permission required
- `/edit_book/` - Change book permission required
- `/can_delete_book_view/` - Delete book permission required
- `/admin_view/` - Admin role required
- `/librarian_view/` - Librarian role required
- `/member_view/` - Member role required

## Usage

1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Run server: `python manage.py runserver`
4. Access views based on user permissions and roles

This implementation satisfies all ALX requirements for Django ORM relationships, custom permissions, and role-based access control.
