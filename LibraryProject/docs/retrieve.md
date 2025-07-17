# Retrieve Operation - Django Shell

## Command to Retrieve a Book Instance

```python
from bookshelf.models import Book

# Retrieve the book by ID
book = Book.objects.get(id=1)

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Output

```
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Other Retrieval Methods

```python
# Retrieve by title
book = Book.objects.get(title="1984")

# Retrieve all books
all_books = Book.objects.all()
print(all_books)

# Retrieve by author
books_by_orwell = Book.objects.filter(author="George Orwell")
print(books_by_orwell)
```

## Output for Other Methods

```
# For all books
<QuerySet [<Book: 1984>]>

# For books by Orwell
<QuerySet [<Book: 1984>]>
```
