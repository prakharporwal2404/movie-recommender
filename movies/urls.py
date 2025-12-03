from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('profile/', views.profile, name='profile'),
    path('recommend/', views.recommend, name='recommend'),
    path('search/', views.search, name='search'),
    path('genre/<str:genre_name>/', views.genre_movies, name='genre_movies'),

    # --- NEW AUTHENTICATION URLS ---
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User Interaction URLs
    path('rate/<int:movie_pk>/<int:rating>/', views.rate_movie, name='rate_movie'),
    path('watchlist/add/<int:movie_pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:movie_pk>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('profile/update/', views.update_profile, name='update_profile'), # Assuming this exists
]
