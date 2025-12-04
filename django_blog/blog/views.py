from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
# New imports for Class-Based Views (CBVs)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CustomUserCreationForm, ProfileEditForm, PostForm
from .models import Post
# Create your views here.

# --- CRUD Views for Post Model ---

class PostListView(ListView):
    """Displays a list of all published blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date'] # Show newest posts first

class PostDetailView(DetailView):
    """Displays a single blog post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create a new post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # Redirect to the detail page of the newly created post
    success_url = reverse_lazy('blog:post_list') 

    def form_valid(self, form):
        # Automatically set the author to the currently logged-in user
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been successfully created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the author of a post to edit it."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def get_success_url(self):
        # Redirect back to the detail view of the updated post
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    # Test function to ensure only the author can edit
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your post has been successfully updated!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the author of a post to delete it."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list') # Redirect to the list after deletion

    # Test function to ensure only the author can delete
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# --- User Registration View ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful registration
            login(request, user) 
            messages.success(request, 'Registration successful! Welcome to the blog.')
            return redirect('blog:profile') # Redirect to profile page
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'blog/register.html', context)

# --- User Profile View (Requires Authentication) ---
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('blog:profile')
        else:
            messages.error(request, 'Error updating your profile. Please check the form.')
    else:
        # Pre-populate the form with current user data
        form = ProfileEditForm(instance=request.user) 

    context = {'form': form}
    return render(request, 'blog/profile.html', context)