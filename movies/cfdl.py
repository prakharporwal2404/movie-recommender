import random
import numpy as np
from django.db.models import Count
# Assuming you have the following models imported/available in your project setup
from .models import Movie, UserProfile, Watchlist, RecentlyViewed 

# --- DEEP LEARNING / COLLABORATIVE FILTERING COMPONENTS ---

# Dimension of the latent factor space (Embedding size)
EMBEDDING_DIM = 50 

# --- SIMULATION FUNCTIONS ---

def get_simulated_user_embedding(user_id):
    """
    Simulates retrieving a User Embedding (Vu). 
    """
    # Use a fixed seed based on user_id to ensure consistent results for the same user
    random.seed(hash(user_id) % 10000)
    # Generate a random vector of EMBEDDING_DIM size
    return np.random.rand(EMBEDDING_DIM)

def get_simulated_movie_embedding(movie_pk):
    """
    Simulates retrieving a single Movie Embedding (Vi).
    """
    # Use a fixed seed based on movie_pk to ensure consistent vector for the movie
    random.seed(hash(movie_pk) % 10000 + 5000)
    return np.random.rand(EMBEDDING_DIM)

def get_simulated_movie_embeddings():
    """
    Simulates retrieving Movie Embeddings (Vi) for all movies. 
    Returns a dictionary: {movie_id: vector}
    """
    movie_embeddings = {}
    for movie in Movie.objects.all():
        movie_embeddings[movie.pk] = get_simulated_movie_embedding(movie.pk)
    return movie_embeddings

def calculate_cf_scores(user_embedding, all_movie_embeddings, watched_movie_ids):
    """
    Core CF/DL prediction step: Calculates the predicted score for each movie.
    """
    scores = {}
    
    for movie_pk, movie_embed in all_movie_embeddings.items():
        if movie_pk in watched_movie_ids:
            # Filtering: Skip movies the user has already interacted with
            continue
        
        # Score Calculation: Vu . Vi
        score = np.dot(user_embedding, movie_embed)
        scores[movie_pk] = score
        
    # Ranking: Sort movies by predicted score (highest score = best prediction)
    ranked_recommendations = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    # Return top 5 movie IDs and their scores
    return ranked_recommendations[:5]

# --- CF/DL ANALYSIS FUNCTION (NEW) ---

def get_cf_analysis(user, movie):
    """
    Calculates the detailed CF analysis data for a single movie.
    """
    user_embed = get_simulated_user_embedding(user.pk)
    movie_embed = get_simulated_movie_embedding(movie.pk)
    
    # Calculate the prediction score
    score = np.dot(user_embed, movie_embed)
    
    # Prepare vectors for display (truncate to first 5 elements and format)
    user_vector_display = [f"{x:.4f}" for x in user_embed[:5]]
    movie_vector_display = [f"{x:.4f}" for x in movie_embed[:5]]
    
    return {
        "score": f"{score:.4f}",
        "user_vector": user_vector_display,
        "movie_vector": movie_vector_display,
        "embedding_dim": EMBEDDING_DIM,
        "reason": f"Predicted affinity score calculated via the dot product of the {EMBEDDING_DIM}-dimension User Embedding and Movie Embedding."
    }

# --- MAIN RECOMENDER FUNCTION (UPDATED) ---

def generate_recommendations_cfdl(user):
    """
    Executes the full CF+DL simulation workflow and returns structured results.
    """
    
    user_id = user.pk
    
    watched_movie_ids = set(
        RecentlyViewed.objects.filter(user=user).values_list('movie__pk', flat=True)
    ).union(
        Watchlist.objects.filter(user=user).values_list('movie__pk', flat=True)
    )

    user_embed = get_simulated_user_embedding(user_id)
    all_movie_embeds = get_simulated_movie_embeddings()
    
    top_predictions = calculate_cf_scores(user_embed, all_movie_embeds, watched_movie_ids)
    
    top_movie_pks = [pk for pk, score in top_predictions]

    final_recommendations = []
    
    movies_by_pk = {movie.pk: movie for movie in Movie.objects.filter(pk__in=top_movie_pks)}

    for pk, score in top_predictions:
        movie = movies_by_pk.get(pk)
        if movie:
            final_recommendations.append({
                # CRITICAL: Include PK for the "View Details" link to work
                "pk": pk, 
                "title": movie.title,
                "genre": getattr(movie, 'genre', 'Unknown Genre'), 
                "score": f"{score:.4f}",
                "reason": f"Predicted score: {score:.4f}. High similarity found between your embedding and this movie's vector based on Collaborative Filtering.",
            })
    
    return final_recommendations
