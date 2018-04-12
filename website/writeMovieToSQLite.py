import sqlite3
conn = sqlite3.connect('tmdb.db')
cur = conn.cursor()
for index, row in movies.iterrows():
    cur.execute('insert into movies (tmdb_id, popularity, director_name, actor_1, actor_2, vote_average, plot_keywords, movie_title) values (?,?,?,?,?,?,?,?)', (row['id'], row['popularity'], row['director_name'], row['actor_1_name'], row['actor_2_name'], row['vote_average'], row['plot_keywords'], row['movie_title']))
conn.commit()
cur.close()
conn.close()
