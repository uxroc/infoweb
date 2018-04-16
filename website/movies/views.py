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
