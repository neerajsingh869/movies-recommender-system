import streamlit as st
import pickle
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    # get the response
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e99d73090f8dbb877439112a9eae37dd&language=en-US")
    # Converting response into json file
    json_data = response.json()
    # return the poster image
    return "http://image.tmdb.org/t/p/w500/" + json_data["poster_path"]

# Now, we are going to recommend 5 movies that are most similar to the given movie
def recommend(movie):
    movie_index = movies_data[movies_data["title"] == movie].index[0]
    distances = similarity[movie_index]
    # 5 tuples, each will have index of movie and it's similarity score w.r.t to movie given
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x: x[1])[1:6]
    recommendations = []
    recommendations_posters = []
    for i in movies_list:
        # store movie names in list
        recommendations.append(movies_data.loc[i[0]]["title"])
        movie_id = movies_data.loc[i[0]]["movie_id"]
        # fetch poster and store it in list
        recommendations_posters.append(fetch_poster(movie_id))
    return recommendations, recommendations_posters

# Loading pickle files
movies_data = pickle.load(open("pickle_files/movies_tfidf.pkl", "rb"))
similarity = pickle.load(open("pickle_files/similarity_scores_tfidf.pkl", "rb"))

movies = movies_data["title"].values
st.title("Movie Recommender System")
selected_movie_name = st.selectbox(
    "Which movie you are interested at?",
    (movies)
)

if st.button("Recommend"):
    movies, posters = recommend(selected_movie_name)
    counter = 0
    for i in st.columns(5):
        with i:
            st.text(movies[counter])
            st.image(posters[counter])
        counter+=1