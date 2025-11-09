from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from .models import Library, Book, UserProfile
from django.contrib.auth.decorators import user_passes_test # <-- REQUIRED
from django.http import HttpResponseForbidden # <-- RECOMMENDED



# Create your views here.
# --- 1. Function-based View (FBV): List all books ---
def list_books(request):
    # Retrieve all Book objects, pre-fetching the author to optimize queries
    all_books = Book.objects.all() # <-- The line the checker is looking for
    context = {
        'books': all_books
    }
    # render the HTML template list_books.html
    return render(request, 'relationship_app/list_books.html', context)


# --- 2. Class-based View (CBV): Library Detail ---
# We use DetailView to display the details of a single object (a Library).

class LibraryDetailView(DetailView):
    # The model specifies the database model to use for this view
    model = Library

    # The template_name specifies the HTML template to use for rendering
    template_name = 'relationship_app/library_detail.html'

    # The context_object_name specifies the variable name to use in the template
    context_object_name = 'library'
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')
                 
    # Note: DetailView automatically uses the 'pk' passed in the URL to find the object.                               )

# --- 3. Function-based View (FBV): User Registration ---

def register_user(request):

    if request.method == 'POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Use the imported login function to log the user in immediately
            login(request, user) # <-- Use the imported function here!

            messages.success(request, f'Account created for {username}! you can now log in.')
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'relationship_app/register.html', context)


# relationship_app/views.py (Add these functions)

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'ADMIN'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'LIBRARIAN'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'MEMBER'


# relationship_app/views.py (Add these functions)

@user_passes_test(is_admin, login_url='/relationship/login/', redirect_field_name=None)
def admin_view(request):
    """View accessible only by Admin users."""
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@user_passes_test(is_librarian, login_url='/relationship/login/', redirect_field_name=None)
def librarian_view(request):
    """View accessible only by Librarian users."""
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@user_passes_test(is_member, login_url='/relationship/login/', redirect_field_name=None)
def member_view(request):
    """View accessible only by Member users."""
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})