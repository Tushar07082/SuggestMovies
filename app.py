import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e5586025eb4140b3ba7dde2c55406732'.format(movie_id))
        data = response.json()
        # st.text(data)
        return 'https://image.tmdb.org/t/p/original'+ data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        #fetch poster form api

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters



movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender system')

selected_movie_name = st.selectbox(
        'Which movie did you like?',
        (movies['title'].values)
)

if st.button('Recommend'):
        names,poster = recommend(selected_movie_name)


        col = st.columns(5)

        for i in range(5):
                with col[i]:
                        st.text(names[i])
                        st.image(poster[i])

