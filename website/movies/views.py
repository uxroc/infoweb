# f-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .recommender import Recommender

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView

import json

from .models import Movie

recommender = None

class MovieList(ListView):
    model = Movie
    template_name = "index.html"

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
        return HttpResponse("Not Get.")
