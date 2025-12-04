from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Post

# Get the active User model (usually django.contrib.auth.models.User)
User = get_user_model()

# --- Registration Form ---
class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form that adds email as a required field.
    """
    email =forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model =User
        fields = UserCreationForm.Meta.fields + ('email',)
# --- Profile Edit Form ---
class ProfileEditForm(forms.ModelForm):
    """
    Form for authenticated users to edit their email and first/last names.
    """
    class Meta:
        model =User
        fields = ('first_name', 'last_name', 'email')

class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post objects.
    """
    class Meta:
        model = Post
        # We explicitly exclude 'author' and 'published_date' as they are set automatically in the view.
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter your post title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your blog post content here'}),
        }

