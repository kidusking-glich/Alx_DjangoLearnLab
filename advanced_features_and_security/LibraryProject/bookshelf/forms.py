from django import forms

class ExampleForm(forms.Form):
    """
    A simple form used to demonstrate Django's forms system.
    This helps in safely validating and sanitizing user input 
    to prevent XSS and other injection attacks.
    """
    name = forms.CharField(
        label='Your Name', 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    message = forms.CharField(
        widget=forms.Textarea
    )
    # bookshelf/forms.py

from django import forms
# import bleach # Requires: pip install bleach

class ExampleForm(forms.Form):
    # ... (name, email, message fields remain the same) ...

    def clean_message(self):
        """
        Security Measurement: Sanitize the message field.
        This is a defense-in-depth measure, especially if you ever use the 
        'safe' filter in a template, which should generally be avoided.
        """
        message = self.cleaned_data['message']
        
        # Example using simple strip for leading/trailing whitespace
        message = message.strip()
        
        # Example using bleach (best practice for allowing LIMITED HTML)
        # allowed_tags = ['b', 'i', 'em', 'strong']
        # message = bleach.clean(message, tags=allowed_tags, strip=True)
        
        # Add a custom check to prevent overly long input (DoS prevention)
        if len(message) > 500:
            raise forms.ValidationError("Message is too long (max 500 characters).")
            
        return message