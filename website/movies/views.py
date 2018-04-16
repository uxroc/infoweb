# f-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .recommender import Recommender
from .query_search import SearchQuery

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView

import json

from .models import Movie

class MovieList(ListView):

    template_name = "index.html"

    paginate_by = 8

    def get_queryset(self):

        if 'recommendation' in self.request.GET:
            recommender = Recommender()

            id = int(self.request.GET['recommendation'])

            recommendation = list(recommender.get_recommendation(id))

            return Movie.objects.filter(pk__in=recommendation)
        elif 'search' in self.request.GET:
            searcher = SearchQuery()
            searcher.index_df()

            query = self.request.GET['search']

            results = searcher.search_result(query)[:20]

            return Movie.objects.filter(tmdb_id__in=results)

        return Movie.objects.all()

def getSearch(request):
    global searcher

    if request.method == 'GET':
        if searcher is None:
            searcher = SearchQuery()
            if not searcher._bt:
                searcher.index_df()

        query = request.GET['query']
        ret = searcher.search_result(query)

        data = []
        for movie_id in ret:
            item = Movie.objects.get(tmdb_id=movie_id)
            data.append({'movie_title' : item.movie_title, 'vote_average' : item.vote_average})

        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Didn't GET it.")

def getRecommendation(request):
    global recommender

    if request.method == 'GET':
        if recommender is None:
            recommender = Recommender()
            print('None')

        movie_id = int(request.GET["id"])
        recommendation = recommender.get_recommendation(movie_id)

        data = []
        for id in recommendation:
            item = Movie.objects.get(pk=id)
            data.append({'movie_title' : item.movie_title, 'vote_average' : item.vote_average})

        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Didn't GET it.")
