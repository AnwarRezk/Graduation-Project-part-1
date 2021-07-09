from django.conf import settings
import pandas as pd

def get_movie_recommendation(movie_name):
    try:
        n_movies_to_reccomend = 5
        movie_list = settings.CAMOVIES_DF[settings.CAMOVIES_DF['name_eg'].str.contains(movie_name)]
        if len(movie_list):
            movie_idx= movie_list.iloc[0]['id']
            movie_idx = settings.CAMOVIE_USER_MAT[settings.CAMOVIE_USER_MAT['movie_id'] == movie_idx].index[0]
            distances , indices = settings.KNN.kneighbors(settings.CSR_DATA[movie_idx],n_neighbors=n_movies_to_reccomend+1)
            rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
            recommend_frame = []
            for val in rec_movie_indices:
                movie_idx = settings.CAMOVIE_USER_MAT.iloc[val[0]]['movie_id']
                idx = settings.CAMOVIES_DF[settings.CAMOVIES_DF['id'] == movie_idx].index
                recommend_frame.append({'Title':settings.CAMOVIES_DF.iloc[idx]['name_eg'].values[0],'Distance':val[1]})
            df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
            return df.to_dict(orient="list")
        else:
            return {"Title": []}
    except:
        return {"Title": []}

# print(get_movie_recommendation('al ekhteyar'))