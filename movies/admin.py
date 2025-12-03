from django.contrib import admin
from .models import Movie, UserProfile, Watchlist, RecentlyViewed, SimpleRating

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','year','genres')
    search_fields = ('title','actors','director','genres')

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','mood','favorite_genres')

admin.site.register(Watchlist)
admin.site.register(RecentlyViewed)
admin.site.register(SimpleRating)
