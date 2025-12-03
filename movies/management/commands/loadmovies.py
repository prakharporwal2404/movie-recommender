from django.core.management.base import BaseCommand
from movies.models import Movie
from movies.utils import load_movie_data_from_json # Reusing your data loader

class Command(BaseCommand):
    help = 'Loads movie data from the sample_movies.json file into the Movie model.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting movie data loading...'))
        movie_data_list = load_movie_data_from_json()
        
        if not movie_data_list:
            self.stdout.write(self.style.ERROR('No movie data found or file path is incorrect. Cannot load data.'))
            return

        movies_processed = 0
        for movie_data in movie_data_list:
            
            # --- Map JSON Keys to Model Fields ---
            
            # Use "rating" key from JSON for initial_rating field
            initial_rating = movie_data.get("rating", 0.0) 
            
            # Ensure genres is a pipe-separated string for easy storage/lookup
            genres_data = movie_data.get("genres", "")
            if isinstance(genres_data, list):
                genres_str = "|".join(genres_data)
            else:
                genres_str = genres_data

            # Use "cast" key from JSON
            cast_str = movie_data.get("cast", "")
            
            # Create or update the movie object
            movie, created = Movie.objects.update_or_create(
                title=movie_data.get("title", f"Untitled Movie {movies_processed}"),
                defaults={
                    'year': movie_data.get("year"),
                    'genres': genres_str,
                    'description': movie_data.get("description", ""),
                    'cast': cast_str,
                    'director': movie_data.get("director", ""),
                    'initial_rating': initial_rating, 
                    'poster_url': movie_data.get("poster_url", ""),
                    
                    # You may want to drop 'actors' field entirely if using 'cast'
                    # Setting 'actors' equal to 'cast' for compatibility with old views
                    'actors': cast_str, 
                    
                    # Assuming movie_id, trailer_url, and mood_tag are handled if they exist
                }
            )
            
            if created:
                movies_processed += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded or updated {len(movie_data_list)} movies. Created {movies_processed} new movies.'))
