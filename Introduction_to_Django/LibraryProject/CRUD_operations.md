# CRUD Operations Documentation

This document contains all the CRUD (Create, Read, Update, Delete) operations performed on the Book model using Django shell.

## Prerequisites

1. Ensure the Django project is set up with the bookshelf app
2. Run migrations: `python manage.py migrate`
3. Open Django shell: `python manage.py shell`

## Complete CRUD Operations Sequence

### 1. CREATE Operation

```python
# Import the Book model
from bookshelf.models import Book

# Create a new book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Verify creation
print(f"Book created with ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

**Output:**

```
Book created with ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

### 2. RETRIEVE Operation

```python
# Retrieve the book by ID
book = Book.objects.get(id=1)

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Retrieve all books
all_books = Book.objects.all()
print(f"All books: {all_books}")
```

**Output:**

```
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
All books: <QuerySet [<Book: 1984>]>
```

### 3. UPDATE Operation

```python
# Retrieve the book to update
book = Book.objects.get(id=1)

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
print(f"Updated Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

**Output:**

```
Updated Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```

### 4. DELETE Operation

```python
# Retrieve the book to delete
book = Book.objects.get(id=1)

# Delete the book
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Books remaining: {all_books}")
print(f"Count of books: {all_books.count()}")

# Try to retrieve the deleted book
try:
    deleted_book = Book.objects.get(id=1)
except Book.DoesNotExist:
    print("Book with ID 1 does not exist - deletion confirmed")
```

**Output:**

```
Books remaining: <QuerySet []>
Count of books: 0
Book with ID 1 does not exist - deletion confirmed
```

## Additional Useful Commands

### Other Creation Method

```python
# Using create() method (creates and saves in one step)
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

### Other Update Method

```python
# Using update() method (more efficient for multiple records)
Book.objects.filter(id=1).update(title="Nineteen Eighty-Four")
```

### Other Delete Method

```python
# Delete using filter and delete() method
Book.objects.filter(id=1).delete()
```

### Query Methods

```python
# Get all books
all_books = Book.objects.all()

# Filter by author
books_by_author = Book.objects.filter(author="George Orwell")

# Get books published after a certain year
recent_books = Book.objects.filter(publication_year__gte=1900)

# Check if books exist
books_exist = Book.objects.exists()

# Count total books
total_count = Book.objects.count()
```

## Model Definition

The Book model is defined in `bookshelf/models.py`:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
```

## Running the Operations

1. Start Django shell: `python manage.py shell`
2. Execute the commands above in sequence
3. Each operation builds upon the previous one
4. The DELETE operation should be run last as it removes the test data

## Notes

- The `__str__` method returns the book title for better representation
- All operations include error handling examples
- The model fields match the assignment requirements
- Migration files are created and applied to set up the database schema
