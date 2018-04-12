from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_title = models.CharField(max_length=50, blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'
