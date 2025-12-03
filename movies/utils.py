import json
import os
from django.db.models import Avg, F # Import necessary Django DB components

# Get the directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Correct the path assumption to be relative to BASE_DIR if the data is packaged with the app
# If data is truly outside, make sure DATASET_PATH is correct or use settings
DATASET_PATH = os.path.join(BASE_DIR, "data", "sample_movies.json")

# Helper to load data ONLY for the management command
def load_movie_data_from_json():
    # Adjusted path to assume 'data' folder is next to utils.py or handled better
    # If the file path in your prompt is correct, use that:
    # DATASET_PATH = "/home/ghost/pre-prod/django_movie_recommender/data/sample_movies.json" 
    
    # Using the relative path assumes the structure: movies/data/sample_movies.json
    data_file_path = os.path.join(BASE_DIR, ".." , "data", "sample_movies.json")

    try:
        with open(data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("movies", [])
    except FileNotFoundError:
        print(f"ERROR: Dataset not found at {data_file_path}. Cannot load data.")
        return []

# --- Recommendation Logic using Database Models ---

from .models import Movie, UserProfile

def recommend_movies(profile, limit=10):
    # Extract user preferences safely
    liked_genres_str = profile.favorite_genres or ""
    liked_genres = [g.strip().lower() for g in liked_genres_str.split(",") if g.strip()]
    user_mood = profile.mood.lower()

    all_movies = Movie.objects.all().annotate(
        # Calculate the average of user ratings for sorting
        avg_user_rating=Avg('simplerating__rating')
    ).order_by('-initial_rating') # Start with the highest initial rating

    scored_movies = []
    
    if not liked_genres and not user_mood:
        # Default: recommend top-rated movies (based on initial rating or DB average)
        # Prioritize movies with high initial_rating
        return list(all_movies[:limit])

    for movie in all_movies:
        score = 0
        movie_genres = movie.genres.lower()
        movie_mood = movie.mood_tag.lower() if movie.mood_tag else ""

        # 1. Score based on favorite genres
        for g in liked_genres:
            if g in movie_genres:
                score += 1.5 # Weight 1.5

        # 2. Score based on current mood match
        if user_mood and user_mood in movie_mood:
            score += 3.0 # High weight 3.0

        # 3. Score based on dataset rating (Initial_rating)
        score += movie.initial_rating / 10.0

        # 4. Score based on overall User Rating (if available)
        if movie.avg_user_rating:
            score += movie.avg_user_rating * 0.5 # Give some weight to community rating

        scored_movies.append((score, movie))

    # Sort by score (descending)
    scored_movies.sort(reverse=True, key=lambda x: x[0])

    # Return only the Movie objects
    return [movie for score, movie in scored_movies[:limit]]
