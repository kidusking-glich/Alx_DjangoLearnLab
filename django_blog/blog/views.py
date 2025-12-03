from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm, ProfileEditForm
# Create your views here.

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