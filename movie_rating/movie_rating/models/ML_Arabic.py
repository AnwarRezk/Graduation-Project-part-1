import pandas as pd
from django.conf import settings

def recommend_engine(title):

    try:
        # infile1 = open("Arabic_indices", 'rb')
        # indices = pickle.load(infile1)
        # infile1.close()


        # infile2 = open("Arabic_Cosine_Weights", 'rb')
        # cos_sim = pickle.load(infile2)
        # infile2.close()

        #infile3 = open("Arabic_movies_df", 'rb')
        #movies_df = pickle.load(infile3)
        #infile3.close()

        # movies_csv = "Arabic_movies_df.csv"
        # movies_df = pd.read_csv(movies_csv)


        # Get the index of the movie that matches the title
        idx = settings.AINDICES[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(settings.ACOS_SIM[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return settings.AMOVIES_DF['id'].iloc[movie_indices].tolist()
    
    except:
        return []

### cosine sim value are represented with movie name


# temp = recommend_engine('el feel el azraq 2')
# temp = temp.tolist()
# print(temp)
