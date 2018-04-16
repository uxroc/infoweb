from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_title = models.CharField(max_length=50, blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    img_url = models.CharField(max_length=200, blank=True, null=True)
    tmdb_id = models.IntegerField()
    director_name = models.CharField(max_length=200, blank=True, null=True)
    actor_1 = models.CharField(max_length=200, blank=True, null=True)
    actor_2 = models.CharField(max_length=200, blank=True, null=True)
    plot_keywords = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'movies'
