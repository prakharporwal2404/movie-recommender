from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_genres = models.CharField(max_length=200, blank=True)
    favorite_actors = models.CharField(max_length=300, blank=True)
    mood = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username


class Movie(models.Model):
    movie_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    year = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=255, blank=True)      # pipe-separated like Action|Drama
    description = models.TextField(blank=True)
    cast = models.CharField(max_length=512, blank=True)        # comma separated
    director = models.CharField(max_length=255, blank=True)
    initial_rating = models.FloatField(default=0.0)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    actors = models.CharField(max_length=512, blank=True)      # kept from old structure, consider merging with 'cast'
    trailer_url = models.URLField(blank=True)
    mood_tag = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.title
    
    def get_genre_list(self):
        # Assuming your genre loader script formats it correctly (Action|Drama)
        return [g.strip() for g in self.genres.split('|') if g.strip()]


class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recent_views")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'movie') 

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','movie')

class SimpleRating(models.Model):
    """Explicit rating by user (1-5)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1..5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','movie')
