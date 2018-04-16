from sklearn.metrics.pairwise import cosine_similarity
from .tfidf import *
from .import_data import *
import numpy as np
from scipy.stats import norm
import os.path

class Recommender:

    def __init__(self):
        # load data
        movies = load_tmdb_movies('tmdb_5000_movies.csv')
        credits = load_tmdb_credits('tmdb_5000_credits.csv')
        self.tmdb = convert_to_original_format(movies, credits)
        self.compute_similairity()
        self.compute_ratings()

    def compute_similairity(self):
        # collect tfidf vectors
        if os.path.exists('similarity.npy'):
            self.similarity = np.load('similarity.npy')
            return

        overview_vec = tf_idf(self.tmdb, 'overview', text_tokenize)
        keyword_vec = tf_idf(self.tmdb, 'plot_keywords', keyword_tokenize)
        genres_vec = tf_idf(self.tmdb, 'genres', keyword_tokenize)

        actor1_vec = tf_idf(self.tmdb, 'actor_1_name', 'zero')
        actor2_vec = tf_idf(self.tmdb, 'actor_2_name', 'zero')
        actor3_vec = tf_idf(self.tmdb, 'actor_3_name', 'zero')
        actor_vec = np.hstack((actor1_vec, actor2_vec, actor3_vec))

        director_vec = tf_idf(self.tmdb, 'director_name', 'zero')
        title_vec = tf_idf(self.tmdb, 'movie_title', 'mean')
        # compute cosine similarity
        # TODO: need a better way to combine the features
        vec = np.hstack((overview_vec, keyword_vec, genres_vec, actor_vec, director_vec, title_vec))

        self.similarity = cosine_similarity(vec, vec)
        np.save('similarity', self.similarity)

    def compute_ratings(self):

        if os.path.exists('ratings.npy'):
            self.ratings = np.load('ratings.npy')
            return

        imdb = np.array(self.tmdb.popularity)
        avgs = np.array(self.tmdb.vote_average)
        yrs = np.array(self.tmdb.title_year)

        avgs_pdf = norm.pdf(avgs, loc=10, scale=3)
        avgs_pdf = avgs_pdf / norm.pdf(10, loc=10, scale=3)

        yrs[np.where(np.isnan(yrs))] = 2018

        yrs_pdf = norm.pdf(yrs, loc=2018, scale=10)
        yrs_pdf = yrs_pdf / norm.pdf(2018, loc=2018, scale=10)

        #self.ratings = imdb
        self.ratings = imdb**2 * avgs_pdf * yrs_pdf
        np.save('ratings', self.ratings)

    def get_similarity(self, id):
        return self.similarity[id, :]

    def get_rating(self):
        return self.ratings

    def get_recommendation(self, id):

        id -= 1

        similarity = self.get_similarity(id)
        ratings = self.get_rating()

        #TODO: need a better way to combine similarity and popularity
        id_list = similarity.argsort()
        similar_id_list = id_list[-20:].astype(int)
        other_id_list = id_list[:-20].astype(int)

        ratings[other_id_list] = 0
        ret = ratings.argsort()[-20:][::-1]
        ret += 1

        return ret


    def get_info(self, id):
        return self.tmdb.original_title[id], self.tmdb.popularity[id]


def main():

    movie_id = int(input("please input the movie id: "))

    recommender = Recommender()
    recommendation = recommender.get_recommendation(movie_id)

    print('The queried movie is: ', recommender.get_info(movie_id)[0])

    print('Recommendations are:')
    for id in recommendation:
        print(recommender.get_info(id))


if __name__ == '__main__':
    main()
