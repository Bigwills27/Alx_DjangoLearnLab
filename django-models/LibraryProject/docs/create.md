# Create Operation - Django Shell

## Command to Create a Book Instance

```python
from bookshelf.models import Book

# Create a new book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output

```python
# The book instance is created and saved to the database
# Returns the created book object with auto-generated ID
```

## Verification

```python
# Check if the book was created successfully
print(f"Book created with ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output

```
Book created with ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```
