#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


# https://files.grouplens.org/datasets/movielens/ml-25m.zip

movies = pd.read_csv(r"C:\Users\User\Downloads\movies.csv")


# In[4]:


movies


# In[5]:


import re

def clean_title(title):
    if isinstance(title, str):
        return re.sub("[^a-zA-Z0-9\s]", "", title)
    else:
        return ""

movies["clean_title"] = movies["title"].fillna("").apply(clean_title)


# In[6]:


movies


# In[7]:


get_ipython().system('pip install --upgrade --force-reinstall scikit-learn')


# In[8]:


import sklearn


# In[9]:


import sys
print(sys.executable)


# In[10]:


from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(ngram_range=(1,2))

tfidf = vectorizer.fit_transform(movies["clean_title"])


# In[18]:


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(title):
    title = "Toy Story 1995"
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices][::-1]
    return results


# In[14]:


query_vec


# In[15]:


similarity


# In[16]:


indices


# In[19]:


results


# In[20]:


import ipywidgets as widgets
from IPython.display import display

movie_input = widgets.Text(
    value = "Toy Story",
    description = "Movie Title:",
    disabled = False
)
movie_list = widgets.Output()

def on_type(data):
    with movie_list:
        movie_list.clear_output() 
        title = data["new"]
        if len(title) > 5:
            display(search(title))

movie_input.observe(on_type, names='value')

display(movie_input, movie_list)


# In[21]:


ratings = pd.read_csv(r"C:\Users\User\Downloads\ratings.csv")


# In[22]:


ratings


# In[23]:


ratings.dtypes


# In[24]:


movie_id = 1


# In[25]:


similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()


# In[26]:


similar_users


# In[27]:


similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]


# In[28]:


similar_user_recs


# In[29]:


similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

similar_user_recs = similar_user_recs[similar_user_recs > .1]


# In[30]:


similar_user_recs


# In[31]:


all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]


# In[32]:


all_users_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())


# In[33]:


all_users_recs


# In[34]:


rec_percentages = pd.concat([similar_user_recs, all_users_recs], axis = 1)
rec_percentages.columns = ["similar", "all"]


# In[35]:


rec_percentages


# In[36]:


rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]


# In[37]:


rec_percentages = rec_percentages.sort_values("score", ascending = False)


# In[38]:


rec_percentages


# In[40]:


# Assuming you want to merge on the index
result = pd.concat([rec_percentages.head(10), movies], axis=1)


# In[48]:


result.head(10)


# In[59]:


def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_users_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    
    rec_percentages = pd.concat([similar_user_recs, all_users_recs], axis = 1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    
    rec_percentages = rec_percentages.sort_values("score", ascending = False)
    return pd.concat([rec_percentages.head(10), movies], axis=1) [["score", "title", "genres;;"]]


# In[60]:


movie_name_input = widgets.Text(
    value="Toy Story",
    description="Movie Title:",
    disabled = False
)

recommendation_list = widgets.Output()

def on_type(data):
    with recommendation_list:
        recommendation_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            results = search(title)
            movie_id = results.iloc[0]["movieId"]
            display(find_similar_movies(movie_id))
            
movie_name_input.observe(on_type, names="value")

display(movie_name_input, recommendation_list)


# In[ ]:




