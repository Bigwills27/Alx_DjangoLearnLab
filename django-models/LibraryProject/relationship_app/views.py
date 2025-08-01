from django.shortcuts import render, redirect
from .models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required

# Create your views here.

# Function-based view to list all books
def list_books(request):
    """Function-based view that lists all books stored in the database"""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for library details
class LibraryDetailView(DetailView):
    """Class-based view that displays details for a specific library"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    

#Setup User Authentication Views

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect ("index")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

#User Login View
class CustomLoginView(LoginView):
    template_name = "login.html"

#user Logout View
class CustomLogoutView(LogoutView):
    template_name = "logout.html"

#Homepage View
def index(request):
    return render(request, "index.html")

#Setting Up Role-Based Views
#Checks if user is Admin
def is_admin(user):
    return user.userprofile.role == 'Admin'

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

#Checks if user is Librarian
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

@login_required
@user_passes_test(is_librarian)

def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

#Checks if user is a Member
def is_member(user):
    return user.userprofile.role == 'Member'

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

#Views to Enforce Permissions
@permission_required("relationship_app.can_add_book")
def can_add_book_view(request):
    return render(request, 'relationship_app/can_add_book.html')

@permission_required("relationship_app.can_change_book")
def can_change_book_view(request):
    return render(request, 'relationship_app/can_change_book.html')

@permission_required("relationship_app.can_delete_book")
def can_delete_book_view(request):
    return render(request, 'relationship_app/can_delete_book.html')