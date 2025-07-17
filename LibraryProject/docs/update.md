# Update Operation - Django Shell

## Command to Update a Book Instance

```python
from bookshelf.models import Book

# Retrieve the book to update
book = Book.objects.get(id=1)

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
print(f"Updated Title: {book.title}")
```

## Output

```
Updated Title: Nineteen Eighty-Four
```

## Other Update Methods

```python
# Using update() method (more efficient for multiple records)
Book.objects.filter(id=1).update(title="Nineteen Eighty-Four")

# Retrieve and display updated book
updated_book = Book.objects.get(id=1)
print(f"Title after update: {updated_book.title}")
print(f"Author: {updated_book.author}")
print(f"Publication Year: {updated_book.publication_year}")
```

## Output for Other Method

```
Title after update: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```
