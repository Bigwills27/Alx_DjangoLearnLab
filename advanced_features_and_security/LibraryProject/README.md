# Advanced Django Features and Security

This Django project demonstrates advanced features including custom user models, permissions management, and security best practices as specified in the ALX curriculum.

## Project Overview

This project is a duplicate of the `django-models` directory, renamed to `advanced_features_and_security` as per ALX Task 0 requirements. It implements:

1. **Custom User Model**: Extended Django's AbstractUser with additional fields
2. **Permissions and Groups**: Role-based access control system
3. **Security Best Practices**: Secure configurations and CSRF protection
4. **HTTPS and Secure Settings**: Production-ready security configurations

## Project Structure

```
LibraryProject/
├── manage.py
├── LibraryProject/
│   ├── settings.py          # Secure settings configuration
│   ├── urls.py
│   └── wsgi.py
└── bookshelf/
    ├── models.py            # Custom user model and permissions
    ├── views.py             # Permission-protected views
    ├── admin.py             # Custom user admin
    ├── forms.py             # Secure forms with validation
    ├── groupaction.py       # Group and permission management
    └── templates/           # CSRF-protected templates
```

---

# **Task 0: Custom User Model Implementation**

## **Overview**

Implemented a custom user model extending Django's `AbstractUser` to include additional fields specific to application needs.

### **Custom User Model Fields**

```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
```

### **Custom User Manager**

```python
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
```

### **Settings Configuration**

```python
# settings.py
AUTH_USER_MODEL = 'bookshelf.CustomUser'
```

---

# **Task 1: Managing Permissions and Groups**

## **Overview**

Implemented role-based access control using Django's Group and Permission models to control access to various application features.

### **Custom Permissions in Models**

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

### **Groups and Permissions Setup**

The `groupaction.py` script creates three groups with specific permissions:

- **Admins**: Full access (can_view, can_create, can_edit, can_delete)
- **Editors**: Moderate access (can_view, can_create, can_edit)
- **Viewers**: Read-only access (can_view)

### **Permission-Protected Views**

```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # Implementation details...

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # Implementation details...

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    # Implementation details...
```

---

# **Task 2: Security Best Practices**

## **Overview**

Implemented comprehensive security measures to protect against common vulnerabilities including XSS, CSRF, and other security threats.

### **Secure Django Settings**

```python
# Production Security Settings
DEBUG = False  # Always False in production

# Browser Security Headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Secure Cookies (HTTPS only)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

### **CSRF Protection**

All forms include CSRF tokens for protection against Cross-Site Request Forgery:

```html
<form method="post">
  {% csrf_token %}
  <!-- Form fields -->
</form>
```

### **Input Validation and Sanitization**

```python
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'author']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title is required")
        return title

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) != 13:
            raise forms.ValidationError("ISBN must be 13 characters long")
        return isbn
```

---

# **Task 3: HTTPS and Secure Redirects**

## **Overview**

Configured Django for secure HTTPS communication and implemented security headers to protect against various attacks.

### **HTTPS Enforcement Settings**

```python
# HTTPS Settings
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional Security Headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### **Security Headers Implemented**

1. **X-Frame-Options**: Set to "DENY" to prevent clickjacking
2. **X-Content-Type-Options**: Set to "nosniff" to prevent MIME-sniffing attacks
3. **X-XSS-Protection**: Enables browser's XSS filtering
4. **HSTS Headers**: Enforces HTTPS for specified duration

---

# **Setup and Usage**

## **Installation**

1. **Navigate to Project Directory**:

   ```bash
   cd advanced_features_and_security/LibraryProject
   ```

2. **Apply Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**:

   ```bash
   python manage.py createsuperuser
   ```

4. **Set Up Groups and Permissions**:

   ```bash
   python manage.py shell
   >>> exec(open('bookshelf/groupaction.py').read())
   ```

5. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## **Testing Permissions**

1. Create test users in Django admin
2. Assign users to different groups (Admins, Editors, Viewers)
3. Log in as different users to test permission enforcement
4. Verify that users can only access features allowed by their permissions

## **Security Features Verified**

- ✅ Custom user model with additional fields
- ✅ Role-based access control with Groups and Permissions
- ✅ CSRF protection on all forms
- ✅ Input validation and sanitization
- ✅ Secure HTTP headers
- ✅ HTTPS enforcement settings
- ✅ Secure cookie settings
- ✅ Production-ready security configurations

## **Files Modified/Created**

- `models.py`: Custom user model and permissions
- `admin.py`: Custom user admin interface
- `views.py`: Permission-protected views
- `forms.py`: Secure forms with validation
- `settings.py`: Comprehensive security settings
- `groupaction.py`: Group and permission management
- `templates/`: CSRF-protected templates

This implementation satisfies all ALX requirements for advanced Django features and security practices.

---ermissions and Groups in Django\*\*

## **Overview**

In this documentation, I’ll walk you through how I implemented role-based access control (RBAC) in my Django application using Django's built-in `Group` and `Permission` models. The main goal was to create user roles—`Admins`, `Editors`, and `Viewers`—each with specific permissions related to managing books and libraries in the application. I'll highlight the crucial steps, particularly focusing on the `groupaction.py` script and the necessary modifications to the `models.py` file.

## **1. Defining Custom Permissions in `models.py`**

### **Step 1: Add Custom Permissions**

First, I defined custom permissions in the `Book` and `Library` models to control actions such as viewing, creating, editing, or deleting records. This is done by adding the `Meta` class inside each model.

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('can_view_book', 'Can view book'),
            ('can_create_book', 'Can create book'),
            ('can_edit_book', 'Can edit book'),
            ('can_delete_book', 'Can delete book'),
        ]

class Library(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    class Meta:
        permissions = [
            ('can_view_library', 'Can view library'),
            ('can_create_library', 'Can create library'),
            ('can_edit_library', 'Can edit library'),
            ('can_delete_library', 'Can delete library'),
        ]
```

### **Explanation**

- **Custom Permissions**: These permissions are added to the `Meta` class of each model. For instance, the `Book` model includes permissions for viewing, creating, editing, and deleting book records. Similarly, the `Library` model has its set of permissions.

## **2. Managing Permissions and Groups with `groupaction.py`**

The `groupaction.py` script is the heart of the RBAC setup. It defines the groups and assigns the appropriate permissions to each group.

### **Highlighted Script: `groupaction.py`**

```python
# Import necessary modules for managing groups and permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, CustomUser, Library

# Step 1: Define the groups and their associated permissions
groups_permissions = {
    'Admins': ['can_view_book', 'can_create_book', 'can_edit_book', 'can_delete_book',
               'can_view_library', 'can_create_library', 'can_edit_library', 'can_delete_library'],
    'Editors': ['can_view_book', 'can_create_book', 'can_edit_book',
                'can_view_library', 'can_create_library', 'can_edit_library'],
    'Viewers': ['can_view_book', 'can_view_library']
}

# Step 2: Create groups and assign permissions to them
for group_name, permissions in groups_permissions.items():
    group, created = Group.objects.get_or_create(name=group_name)

    for perm in permissions:
        model_name = perm.split('_')[2]  # Extract model name
        content_type = ContentType.objects.get(model=model_name)
        permission = Permission.objects.get(codename=perm, content_type=content_type)
        group.permissions.add(permission)

    if created:
        print(f'Created group: {group_name}')
    else:
        print(f'Group already exists: {group_name}')

    for perm in permissions:
        print(f' - Added permission: {perm} to group {group_name}')

print('Group and permission setup complete.')
```

### **Explanation**

- **Groups**: The script defines three groups—`Admins`, `Editors`, and `Viewers`. Each group is associated with specific permissions.
- **Permission Assignment**: Permissions are assigned to groups using a loop that extracts the model name from the permission codename and retrieves the relevant `ContentType` and `Permission` objects.

## **3. Testing Permissions in Django Shell**

After setting up the groups and permissions, I used the Django shell to create users and assign them to the appropriate groups. Here’s a brief overview:

```python
>>> from bookshelf.models import CustomUser
>>> from django.contrib.auth.models import Group

# Create test users
>>> CustomUser.objects.create_user(email='user1@example.com', password='password123', username='user1')
>>> CustomUser.objects.create_user(email='user2@example.com', password='password123', username='user2')
>>> CustomUser.objects.create_user(email='user3@example.com', password='password123', username='user3')

# Fetch users and assign them to groups
>>> user1 = CustomUser.objects.get(email='user1@example.com')
>>> user2 = CustomUser.objects.get(email='user2@example.com')
>>> user3 = CustomUser.objects.get(email='user3@example.com')

# Add 'user1' to the 'Editors' group
>>> editors_group = Group.objects.get(name='Editors')
>>> editors_group.user_set.add(user1)

# Add 'user2' to the 'Viewers' group
>>> viewers_group = Group.objects.get(name='Viewers')
>>> viewers_group.user_set.add(user2)

# Add 'user3' to the 'Admins' group
>>> admins_group = Group.objects.get(name='Admins')
>>> admins_group.user_set.add(user3)

# Verify permissions
>>> print(f"Editors group permissions: {[perm.codename for perm in editors_group.permissions.all()]}")
>>> print(f"Viewers group permissions: {[perm.codename for perm in viewers_group.permissions.all()]}")
>>> print(f"Admins group permissions: {[perm.codename for perm in admins_group.permissions.all()]}")
```

## **4. Enforcing Permissions in Views**

I enforced these permissions in my views by using the `@permission_required` decorator.

```python
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def add_book(request):
    # Book creation logic here
    pass

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, book_id):
    # Book editing logic here
    pass

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    # Book deletion logic here
    pass
```

## **5. Setting Up URLs**

The corresponding URLs were defined in 'urls.py' to map these views:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
]
```

## **6. Testing the Setup**

To ensure that everything was working correctly, I performed a series of tests:

1. **Run the `groupaction.py` script**:

   - This script sets up the groups and assigns the permissions. Running it ensures that the correct permissions are assigned to each group.

2. **Register and Login Users**:

   - I created test users and assigned them to different groups (`Admins`, `Editors`, `Viewers`) using the Django Admin panel.

3. **Check Access Control**:

   - I logged in as different users and verified their access to various views (`book_list`, `add_book`, `edit_book`, `delete_book`).

4. **View in Browser**:
   - I checked the HTML pages to ensure that the correct buttons/links appeared based on the user’s permissions.

## **7. Conclusion**

By implementing RBAC in my Django application, I was able to control access to different parts of the application based on user roles. The `groupaction.py` script plays a crucial role in managing these permissions, while the custom permissions defined in `models.py` ensure that access is tightly controlled. Testing these permissions in the Django shell confirmed that the setup works as intended, ensuring a secure and functional application.

---
