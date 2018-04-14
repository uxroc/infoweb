from Recommendation import Preprocessing
from nltk.stem.porter import PorterStemmer
import nltk
from nltk.corpus import stopwords
import os.path
import numpy as np


def keyword_tokenize(text):
    tokens = text.split('|')
    tokens = list(filter(None, tokens))
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    stemmer = PorterStemmer()
    stems = stem_tokens(tokens, stemmer)
    return stems


def text_tokenize(text):
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    stems = stem_tokens(tokens, stemmer)
    return stems


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


class SearchQuery(object):
    def __init__(self):
        self._bt = {}
        self._movies= []
        # load the dataset
        credits = Preprocessing.load_tmdb_credits("D:/WPI/CS525-IR/Project/tmdb_5000_credits.csv")
        movies = Preprocessing.load_tmdb_movies("D:/WPI/CS525-IR/Project/tmdb_5000_movies.csv")
        self.tmdb = Preprocessing.convert_to_original_format(movies, credits)

    def index_df(self):
        if os.path.exists('score.npy'):
            self._bt = np.load('score.npy').item()
            return

        num_movie_indexed = 0
        for index, row in self.tmdb.iterrows():
            num_movie_indexed += 1
            if row['id'] not in self._movies:
                self._movies.append(row['id'])
            score_dict = {}
            overview = text_tokenize(row['overview']) if type(row['overview']) == str else []
            score_dict['overview'] = [overview, 3]
            keywords = keyword_tokenize(row['plot_keywords']) if type(row['plot_keywords']) == str else []
            score_dict['keywords'] = [keywords, 6]
            actor_1_name = text_tokenize(row['actor_1_name']) if type(row['actor_1_name']) == str else []
            score_dict['actor_1_name'] = [actor_1_name, 1.5]
            actor_2_name = text_tokenize(row['actor_2_name']) if type(row['actor_2_name']) == str else []
            score_dict['actor_2_name'] = [actor_2_name, 1.25]
            actor_3_name = text_tokenize(row['actor_3_name']) if type(row['actor_3_name']) == str else []
            score_dict['actor_3_name'] = [actor_3_name, 1]
            director_name = text_tokenize(row['director_name']) if type(row['director_name']) == str else []
            score_dict['director_name'] = [director_name, 2]
            movie_title = text_tokenize(row['movie_title']) if type(row['movie_title']) == str else []
            score_dict['movie_title'] = [movie_title, 20]
            for k,v in score_dict.items():
                for term in v[0]:
                    if term not in self._bt.keys():
                        d = {}
                        d[row['id']] = v[1]
                        self._bt[term] = d
                    else:
                        if row['id'] not in self._bt[term].keys():
                            self._bt[term][row['id']] = v[1]
                        else:
                            self._bt[term][row['id']] += v[1]
        np.save('score', self._bt)
        return num_movie_indexed

    def search_result(self, text):
        result_dict = {}
        for term in text_tokenize(text):
            if self._bt.get(term) != None:
                for k,v in self._bt.get(term).items():
                    if k not in result_dict.keys():
                        result_dict[k] = v
                    else:
                        result_dict[k] += v
        result = sorted(result_dict, key = result_dict.get, reverse=True)
        score_list = []
        for key in result:
            score_list.append(result_dict.get(key))
        return result


def main(args):
    query = str(input("please input the query: "))
    search = SearchQuery()
    print("starting searching")
    num_files = search.index_df()
    print('search results are:')
    print(search.search_result(query))

if __name__ == "__main__":
    import sys
    main(sys.argv)

