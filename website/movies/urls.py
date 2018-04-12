from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MovieList.as_view(), name='movie_list'),
    url(r'^recomm/$', views.getRecommendation, name='get_recommendation'),
]
