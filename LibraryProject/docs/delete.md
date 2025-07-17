# Delete Operation - Django Shell

## Command to Delete a Book Instance

```python
from bookshelf.models import Book

# Retrieve the book to delete
book = Book.objects.get(id=1)

# Delete the book
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Books remaining: {all_books}")
print(f"Count of books: {all_books.count()}")
```

## Output

```
Books remaining: <QuerySet []>
Count of books: 0
```

## Other Delete Methods

```python
# Delete using filter and delete() method
Book.objects.filter(id=1).delete()

# Try to retrieve the deleted book (this will raise an exception)
try:
    deleted_book = Book.objects.get(id=1)
except Book.DoesNotExist:
    print("Book with ID 1 does not exist - deletion confirmed")
```

## Output for Other Method

```
Book with ID 1 does not exist - deletion confirmed
```

## Verification Commands

```python
# Check if any books exist
books_exist = Book.objects.exists()
print(f"Any books exist: {books_exist}")

# Count total books
total_books = Book.objects.count()
print(f"Total books in database: {total_books}")
```

## Verification Output

```
Any books exist: False
Total books in database: 0
```
