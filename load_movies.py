import csv, os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from movies.models import Movie

fn = 'data/sample_movies.csv'
cnt = 0
with open(fn, newline='', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        Movie.objects.update_or_create(
            title=row.get('title') or row.get('Title'),
            defaults={
                'genres': row.get('genres') or row.get('Genres') or '',
                'description': row.get('description') or row.get('overview') or '',
                'actors': row.get('actors') or '',
                'director': row.get('director') or '',
                'year': int(row['year']) if row.get('year') and row['year'].isdigit() else None,
                'trailer_url': row.get('trailer_url') or ''
            }
        )
        cnt += 1
print("Loaded", cnt, "rows")

