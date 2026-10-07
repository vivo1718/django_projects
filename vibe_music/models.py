from django.db import models

class CapsuleDiscovery(models.Model):
    mood_query = models.CharField(max_length=150)
    album_title = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    release_year = models.CharField(max_length=10, blank=True)
    ai_review = models.TextField()
    # Stores the clean youtube search query string
    youtube_search_term = models.CharField(max_length=300)
    discovered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.album_title} - {self.artist_name}"
