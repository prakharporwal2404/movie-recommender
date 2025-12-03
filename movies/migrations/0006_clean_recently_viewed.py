# movies/migrations/0006_clean_recently_viewed.py

from django.db import migrations
from django.db.models import Max

def delete_duplicate_views(apps, schema_editor):
    RecentlyViewed = apps.get_model('movies', 'RecentlyViewed')

    # Identify the primary key (id) of the most recent entry for each user/movie pair
    # We need to exclude these IDs from deletion.
    ids_to_keep = RecentlyViewed.objects.values('user', 'movie').annotate(
        max_id=Max('id')
    ).values_list('max_id', flat=True)

    # Delete all rows whose IDs are NOT in the list of IDs to keep.
    RecentlyViewed.objects.exclude(id__in=ids_to_keep).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_movie_initial_rating_movie_movie_id_and_more'),
    ]

    operations = [
        migrations.RunPython(delete_duplicate_views, migrations.RunPython.noop),
    ]
