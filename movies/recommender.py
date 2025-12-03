from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Movie, UserProfile, RecentlyViewed
import numpy as np
from datetime import timedelta
from django.utils import timezone

# --- Helper: build TF-IDF matrix over enriched text ---
def _build_corpus_and_matrix():
    qs = Movie.objects.all()
    movies = list(qs)
    corpus = []
    for m in movies:
        parts = [m.title or "", m.genres or "", m.description or "", m.actors or "", m.director or ""]
        corpus.append(" ".join(parts))
    tfidf = TfidfVectorizer(stop_words='english', max_features=50000)
    if corpus:
        tfidf_matrix = tfidf.fit_transform(corpus)
    else:
        tfidf_matrix = None
    # maps
    movieid_to_idx = {m.id:i for i,m in enumerate(movies)}
    idx_to_movie = {i:m for i,m in enumerate(movies)}
    return movies, tfidf, tfidf_matrix, movieid_to_idx, idx_to_movie

# cached per-process (simple)
_CACHED = {"movies":None, "tfidf":None, "matrix":None, "map_in":None, "map_out":None}
def _ensure_cache():
    if _CACHED["movies"] is None:
        movies, tfidf, matrix, m2i, i2m = _build_corpus_and_matrix()
        _CACHED.update({"movies":movies,"tfidf":tfidf,"matrix":matrix,"map_in":m2i,"map_out":i2m})

def refresh_cache():
    _CACHED.update({"movies":None, "tfidf":None, "matrix":None, "map_in":None, "map_out":None})
    _ensure_cache()

# Mood -> genre mapping
MOOD_GENRE_MAP = {
    "happy": ["Comedy","Family","Adventure"],
    "dark": ["Thriller","Horror","Mystery","Crime"],
    "romantic": ["Romance","Drama"],
    "intense": ["Action","Thriller"],
    "chill": ["Comedy","Drama","Animation"],
    "mindbending": ["Sci-Fi","Mystery"],
    "action": ["Action","Adventure"]
}

def _mood_score(movie: Movie, mood: str):
    if not mood:
        return 0.0
    target_genres = MOOD_GENRE_MAP.get(mood, [])
    if not target_genres:
        return 0.0
    movie_genres = [g.strip().lower() for g in (movie.genres or "").split("|") if g.strip()]
    score = 0.0
    for tg in target_genres:
        if tg.lower() in movie_genres:
            score += 1.0
    # normalize
    return score / max(1, len(target_genres))

def _actor_director_boost(movie: Movie, fav_actors_list, fav_directors_list):
    score = 0.0
    if fav_actors_list:
        movie_actors = [a.strip().lower() for a in (movie.actors or "").split(",") if a.strip()]
        for a in fav_actors_list:
            if a.strip().lower() in movie_actors:
                score += 0.4   # strong boost
    if fav_directors_list:
        if (movie.director or "").strip().lower() in [d.strip().lower() for d in fav_directors_list]:
            score += 0.25
    return min(1.0, score)

def recommend_for_user(user, topk=10, alpha=0.6):
    """
    Hybrid scoring:
      final = alpha * content_sim_norm + (1-alpha) * extra_score
    extra_score = mood_bonus + actor_director_bonus + recent_similarity_boost
    """
    _ensure_cache()
    movies = _CACHED["movies"]
    matrix = _CACHED["matrix"]
    m2i = _CACHED["map_in"]
    i2m = _CACHED["map_out"]

    if not movies:
        return []

    # user prefs
    profile = None
    try:
        profile = user.profile
    except Exception:
        profile = None

    fav_genres = []
    if profile and profile.favorite_genres:
        fav_genres = [g.strip().lower() for g in profile.favorite_genres.split("|") if g.strip()]

    fav_actors = []
    if profile and profile.favorite_actors:
        fav_actors = [a.strip() for a in profile.favorite_actors.split(",") if a.strip()]

    mood = profile.mood if profile and profile.mood else ""

    # Build candidate pool: popular (most movies) + neighbors of recently viewed
    candidates = set([m.id for m in movies])  # small DB, allow all

    # Compute user's recent viewed top movies (last 30 days)
    recent = RecentlyViewed.objects.filter(user=user, viewed_at__gte=timezone.now()-timedelta(days=365)).order_by('-viewed_at')[:5]
    recent_ids = [r.movie.id for r in recent]

    # If TF-IDF matrix exists, compute content similarity vector to user's recent movies avg vector
    content_scores = {}
    if matrix is not None and recent_ids:
        # average vector of recent movies
        idxs = [m2i[mid] for mid in recent_ids if mid in m2i]
        if idxs:
            user_vec = matrix[idxs].mean(axis=0)
            sims = linear_kernel(user_vec, matrix).flatten()  # similarity to all movies
            for i, s in enumerate(sims):
                mid = i2m[i].id
                content_scores[mid] = float(s)

    # normalize content scores
    if content_scores:
        vals = np.array(list(content_scores.values()))
        minv, maxv = float(vals.min()), float(vals.max())
    else:
        minv, maxv = 0.0, 1.0

    scored = []
    for mid in candidates:
        movie = Movie.objects.get(id=mid)
        # content normalized
        cscore_raw = content_scores.get(mid, 0.0)
        c_norm = (cscore_raw - minv) / (maxv - minv + 1e-9) if maxv>minv else 0.0

        # extra: mood
        mood_bonus = _mood_score(movie, mood)  # 0..1

        # actor/director
        actor_dir = _actor_director_boost(movie, fav_actors, [])  # no fav directors stored now

        # recent similarity boost: if movie is one of recent -> small boost
        recent_boost = 0.3 if mid in recent_ids else 0.0

        extra = min(1.0, mood_bonus*0.6 + actor_dir*0.8 + recent_boost*0.9)

        final = alpha * c_norm + (1 - alpha) * extra

        # small freshness bias: prefer newer movies slightly
        year_bias = 0.0
        if movie.year:
            try:
                year_bias = max(0.0, (movie.year - 2000) / 30.0)  # 0..~1 for 2000-2030
            except Exception:
                year_bias = 0.0
        final = final * 0.9 + year_bias*0.1

        scored.append((movie, float(final), float(c_norm), float(extra)))

    # sort and return topk excluding movies user has in watchlist maybe? keep simple
    scored = sorted(scored, key=lambda x: x[1], reverse=True)[:topk]
    results = []
    for m,f,cn,ex in scored:
        results.append({
            "movie": m,
            "score": f,
            "content_norm": cn,
            "extra": ex
        })
    return results
