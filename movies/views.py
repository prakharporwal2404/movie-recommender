from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q # For aggregation and complex querying
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .utils import recommend_movies
from .models import UserProfile, Movie, Watchlist, SimpleRating, RecentlyViewed
from django.contrib.auth import login, logout, authenticate
from django.db.models import Avg, Count
from django.contrib import messages
from .models import UserProfile, Movie, Watchlist, SimpleRating, RecentlyViewed
from .forms import CustomUserCreationForm, CustomAuthenticationForm # <-- IMPORT FORMS
from .cfdl import generate_recommendations_cfdl, get_cf_analysis
from django.utils import timezone

# --- Authentication Views ---

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            # Create a corresponding UserProfile
            UserProfile.objects.create(user=user)
            
            # Log the user in immediately
            login(request, user)
            messages.success(request, f"Account created for {user.username}! Welcome.")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {
        'form': form,
        'page_title': 'Sign Up'
    })


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                # Redirect to the URL they were trying to access, or 'home'
                return redirect(request.POST.get('next') or 'home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            # Add non-field errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'registration/login.html', {
        'form': form,
        'page_title': 'Login'
    })

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


# ... (Place the rest of your existing view functions below this) ...




def home(request):
    # --- CHANGE START ---
    
    # 1. Fetch movies, order by initial rating (highest first), and slice to get the top 30.
    all_movies = Movie.objects.all().order_by('-initial_rating', 'title')[:30] 

    # 2. Assign the limited queryset to 'trending' for use in the template.
    trending = all_movies 
    
    # --- CHANGE END ---

    # Get all unique genres for the filter list (no change needed here)
    genre_data = Movie.objects.values_list('genres', flat=True).distinct()
    genres = set()
    for genre_str in genre_data:
        for g in genre_str.split('|'):
            if g.strip():
                genres.add(g.strip())
    
    sorted_genres = sorted(list(genres))

    return render(request, "movies/home.html", {
        # 'trending' now contains the top 30 movies
        "trending": trending, 
        "genres": sorted_genres
    })


def search(request):
    q = request.GET.get("q", "")

    if q:
        # Case-insensitive search on movie title
        results = Movie.objects.filter(title__icontains=q).order_by('-initial_rating')
    else:
        results = Movie.objects.none() # Empty queryset if no query

    return render(request, "movies/search.html", {"results": results, "query": q})


def genre_movies(request, genre_name):
    # Filter movies where the 'genres' field contains the specific genre (using SQL LIKE)
    results = Movie.objects.filter(genres__icontains=genre_name).order_by('-initial_rating')
    
    return render(request, "movies/genre.html", {"results": results, "genre_name": genre_name})


def movie_detail(request, pk):
    # Use primary key (pk) or movie_id for robust lookups
    movie = get_object_or_404(Movie, pk=pk)

    user_rating = None
    is_on_watchlist = False
    
    if request.user.is_authenticated:
        # Log recently viewed and update timestamp if already exists
        RecentlyViewed.objects.update_or_create(
            user=request.user, 
            movie=movie,
            defaults={'movie': movie} # Ensures 'movie' is set if created
        )
        
        # Check for existing rating
        user_rating = SimpleRating.objects.filter(user=request.user, movie=movie).first()
        
        # Check for watchlist status
        is_on_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()

    context = {
        "movie": movie,
        "user_rating": user_rating.rating if user_rating else None,
        "is_on_watchlist": is_on_watchlist,
    }

    return render(request, "movies/detail.html", context)



@login_required
def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == "POST":
        rating_value = request.POST.get('rating') # Expecting an integer 1-5
        
        try:
            rating_value = int(rating_value)
            if 1 <= rating_value <= 5:
                SimpleRating.objects.update_or_create(
                    user=request.user, 
                    movie=movie, 
                    defaults={'rating': rating_value}
                )
        except (ValueError, TypeError):
            # Handle invalid rating input
            pass 

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@login_required
def recommend(request):
    """
    Generates personalized CF/DL recommendations by calling the engine 
    and renders the result.
    """
    
    # 1. Get User Profile 
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # 2. Call the CF/DL Recommender Engine 
    # NOTE: The actual import (from .cfdl import generate_recommendations_cfdl)
    # must be placed at the top of the views.py file.
    recs = generate_recommendations_cfdl(request.user)
    
    context = {
        # The key is 'recommended' to match the 'movies/recommend.html' template
        'recommended': recs,
        'user_profile': user_profile 
    }
    
    # 3. Render the correct template
    return render(request, 'movies/recommend.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Assuming you have imported your models and forms
from .models import Movie, UserProfile, Watchlist, RecentlyViewed # Ensure all models are imported
from .forms import UserProfileForm # Ensure UserProfileForm is imported

# Assuming other views like movie_detail, index, etc., are here...

@login_required
def profile(request):
    # This view displays the profile form and lists
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=profile)

    # Fetch Watchlist and Recently Viewed items
    watchlist = Watchlist.objects.filter(user=request.user).order_by('-added_at')
    recent_views = RecentlyViewed.objects.filter(user=request.user).order_by('-viewed_at')

    context = {
        'form': form,
        'watchlist': watchlist,
        'recent_views': recent_views,
    }
    return render(request, "movies/profile.html", context)


@login_required
def update_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # CRITICAL FIX for saving MultipleChoiceField data
            # The form returns a list for favorite_genres. We must join it into a string.
            genres_list = form.cleaned_data.get('favorite_genres', [])
            
            # Join the list back into a comma-separated string for saving to the model
            profile.favorite_genres = ",".join(genres_list)
            profile.current_mood = form.cleaned_data.get('current_mood')
            profile.save()
            
            # Optionally, you might want to use Django messages here for feedback
            return redirect('profile')
    else:
        # If method is GET, the form will correctly load initial data thanks to the forms.py fix
        form = UserProfileForm(instance=profile)
        
    return render(request, "movies/profile.html", {'form': form})


@login_required
def add_to_watchlist(request, movie_pk):
    # Use pk=movie_pk to correctly look up the Movie object
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    # Use get_or_create to prevent duplicates
    Watchlist.objects.get_or_create(user=request.user, movie=movie)

    # Redirect back to the movie detail page or home page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_watchlist(request, movie_pk):
    # FIX for Watchlist removal: use pk=movie_pk to correctly look up the Movie object
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    # Try to delete the Watchlist entry
    Watchlist.objects.filter(user=request.user, movie=movie).delete()

    # Redirect back to the page the user came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# --- MOVIE DETAIL VIEW (UPDATED FOR CF/DL ANALYSIS) ---
@login_required
def movie_detail(request, pk):
    """
    Displays movie details and includes a detailed CF/DL analysis 
    if the user is authenticated.
    """
    movie = get_object_or_404(Movie, pk=pk)
    
    # 1. Track Recently Viewed (Implicit Feedback)
    RecentlyViewed.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={'viewed_at': timezone.now()} # Assuming timezone is imported or mocked
    )
    
    # 2. Check Watchlist Status
    in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()

    # 3. Generate Detailed CF/DL Analysis 
    # This is the new, critical step for the presentation
    cf_analysis = get_cf_analysis(request.user, movie)

    context = {
        'movie': movie,
        'in_watchlist': in_watchlist,
        'cf_analysis': cf_analysis,
    }

    # Renders the new detail template
    return render(request, 'movies/movie_detail.html', context)
