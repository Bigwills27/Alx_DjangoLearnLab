# Django Library Project

This is a Django project for managing a library's book collection, created as part of the ALX Django learning lab.

## Project Structure

```
LibraryProject/
├── manage.py
├── db.sqlite3
├── CRUD_operations.md
├── docs/
│   ├── create.md
│   ├── retrieve.md
│   ├── update.md
│   └── delete.md
├── bookshelf/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
└── LibraryProject/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Book Model

The `Book` model in `bookshelf/models.py` contains:

- `title`: CharField with max_length=200
- `author`: CharField with max_length=100
- `publication_year`: IntegerField

## Setup Instructions

1. **Install Django** (if not already installed):

   ```bash
   pip install django
   ```

2. **Navigate to the project directory**:

   ```bash
   cd LibraryProject
   ```

3. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Access Django shell**:

   ```bash
   python manage.py shell
   ```

## CRUD Operations

All CRUD operations are documented in:

- `CRUD_operations.md` - Complete documentation with examples
- `docs/create.md` - CREATE operation details
- `docs/retrieve.md` - RETRIEVE operation details
- `docs/update.md` - UPDATE operation details
- `docs/delete.md` - DELETE operation details

## Testing the Model

The Book model has been tested with all CRUD operations:

- CREATE: Successfully creates new book instances
- RETRIEVE: Successfully retrieves books by ID and other filters
- UPDATE: Successfully updates book attributes
- DELETE: Successfully deletes book instances

## Example Usage

```python
from bookshelf.models import Book

# Create a book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Retrieve the book
book = Book.objects.get(id=1)

# Update the book
book.title = "Nineteen Eighty-Four"
book.save()

# Delete the book
book.delete()
```

## Features

- Django 4.2.23 compatible
- SQLite database (included)
- Proper model field definitions
- Complete migration files
- Documentation included
- Tested CRUD operations

## Assignment Requirements Completed

- Created bookshelf app using `python manage.py startapp bookshelf`
- Defined Book model with required fields (title, author, publication_year)
- Created and applied migrations
- Documented all CRUD operations
- Tested operations in Django shell
- Created separate markdown files for each operation
- Included CRUD_operations.md with complete documentation

## Author

Created for ALX Django Learning Lab - Introduction to Django assignment.

## Repository Information

- **Repository**: Alx_DjangoLearnLab
- **Directory**: Introduction_to_Django
- **Project**: LibraryProject
