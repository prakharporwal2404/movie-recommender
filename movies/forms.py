from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User




from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile # Make sure to import UserProfile

# --- Define fixed choices for the forms ---

GENRE_CHOICES = [
    ('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), 
    ('Comedy', 'Comedy'), ('Crime', 'Crime'), ('Drama', 'Drama'), 
    ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), 
    ('Romance', 'Romance'), ('Sci-Fi', 'Sci-Fi'), ('Thriller', 'Thriller'),
    ('War', 'War'), ('Western', 'Western'), ('Documentary', 'Documentary'),
]

MOOD_CHOICES = [
    ('Chill', 'Chill & Relaxed'), 
    ('Exciting', 'Exciting & Intense'), 
    ('Serious', 'Serious & Thoughtful'),
    ('Happy', 'Happy & Upbeat'),
    ('Dark', 'Dark & Brooding'),
]

# Assuming other authentication forms are here...

class UserProfileForm(forms.ModelForm):
    # Override the model field to use CheckboxSelectMultiple
    favorite_genres = forms.MultipleChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Favorite Genres'
    )

    current_mood = forms.ChoiceField(
        choices=[('', '--- Select a Mood ---')] + MOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        required=False,
        label='Current Mood'
    )
    
    class Meta:
        model = UserProfile
        fields = ['favorite_genres', 'current_mood']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # CRITICAL FIX for loading initial data for the MultipleChoiceField
        # If the form is bound to an instance, we convert the stored 
        # comma-separated string back into a list so checkboxes appear selected.
        if self.instance and self.instance.pk and self.instance.favorite_genres:
            # Split the comma-separated string into a list of choices
            self.initial['favorite_genres'] = self.instance.favorite_genres.split(',')
        
        # Apply style to the mood select field
        if 'current_mood' in self.fields:
            self.fields['current_mood'].widget.attrs.update({
                'class': 'form-select bg-dark text-white border-secondary'
            })



# --- Signup Form ---
class CustomUserCreationForm(UserCreationForm):
    # Inherits fields (username, password, password2) from UserCreationForm
    class Meta:
        model = User
        fields = ('username', 'email') # Only include email if you want it on signup
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control bg-dark text-white border-secondary'
            })
            
        # Optional: Make email field required if included
        if 'email' in self.fields:
            self.fields['email'].required = True

# --- Login Form ---
class CustomAuthenticationForm(AuthenticationForm):
    
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'placeholder': 'Enter your username'
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'placeholder': 'Enter your password'
        })
    )


class SimpleRatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
