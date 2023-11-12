#%%
import pandas as pd
import numpy as np


#%%
raw_books = pd.read_csv('./data/Books.csv')
raw_ratings = pd.read_csv('./data/Ratings.csv')
raw_users = pd.read_csv('./data/Users.csv')

#%%

# Remove unnecessary columns for books
books = raw_books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]

#%%
## Count the number of ratings each book has received
book_ratings_count = raw_ratings.groupby(by = 'ISBN')['Book-Rating'].count().sort_values(ascending=False)

# Assuming raw_ratings is your DataFrame
book_ratings_summary = raw_ratings.groupby(by='ISBN')['Book-Rating'].agg(['count', 'mean', 'median']).sort_values(by='count', ascending=False)

# Rename the columns for clarity
book_ratings_summary = book_ratings_summary.rename(columns={'count': 'Rating-Count', 'mean': 'Average-Rating', 'median':'Median-Rating'})

## Remove the books that received less than 30 ratings
popular_books = book_ratings_count[book_ratings_summary['Rating-Count'] >= 30]

# %%
## Count the number of ratings each user has given
user_ratings_count = raw_ratings.groupby(by = 'User-ID')['Book-Rating'].count().sort_values(ascending=False)

users_atleast30 = user_ratings_count[user_ratings_count  >= 30]

# %%

## Remove books that are not in popular_books
books_final = books[books['ISBN'].isin(popular_books.index)]

## Remove users that are not in user_atleast30
users_final = raw_users[raw_users['User-ID'].isin(users_atleast30.index)]

## Filter ratings
ratings_final = raw_ratings[(raw_ratings['User-ID'].isin(users_atleast30.index)) | (raw_ratings['ISBN'].isin(popular_books))]

# %%

merged_df = pd.merge(ratings_final, users_final, left_on = 'User-ID', right_on = 'User-ID', how='left')
merged_df = pd.merge(merged_df, books_final, left_on = 'ISBN', right_on = 'ISBN', how='left')

# %%
final_df = merged_df.dropna()


# Assuming raw_ratings is your DataFrame
book_ratings_summary = final_df.groupby(by='ISBN')['Book-Rating'].agg(['count', 'mean', 'median']).sort_values(by='count', ascending=False)

# Rename the columns for clarity
book_ratings_summary = book_ratings_summary.rename(columns={'count': 'Rating-Count', 'mean': 'Average-Rating', 'median':'Median-Rating'})

# %%
book_pivot = final_df.pivot_table(columns = 'User-ID', index = 'Book-Title', values = 'Book-Rating')
# %%
book_pivot.fillna(0, inplace=True)

# %%
### Model training
from scipy.sparse import csr_matrix
# %%
book_sparse = csr_matrix(book_pivot)

# %%
from sklearn.neighbors import NearestNeighbors
model = NearestNeighbors(algorithm='brute')
model.fit(book_sparse)

# %%
# %%
def get_info(book_name):
    subset = books_final[books_final['Book-Title'] == book_name]
    subset = subset.reset_index(drop=True)
    info_dict = dict(subset.iloc[0])  # Convert the first row to a dictionary
    
    rating_count = book_ratings_summary[book_ratings_summary.index == info_dict['ISBN']]['Rating-Count'].values[0]
    average_rating = book_ratings_summary[book_ratings_summary.index == info_dict['ISBN']]['Average-Rating'].values[0]
    average_rating = np.round(average_rating, 1)

    info_dict['Rating Count'] = rating_count
    info_dict['Average Rating'] = average_rating

    return info_dict
# %%
def get_books_same_author(book_name):
    author = books_final.loc[books_final['Book-Title'] == book_name, 'Book-Author'].reset_index(drop=True)[0]
    other_books = books_final.loc[books_final['Book-Author'] == author, 'Book-Title']
    other_books_by_author = list(other_books)
    return other_books_by_author

# %%
def recommend_books(book_name):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)

    recommended_books = []
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            if j == book_name:
                print(f"You search '{book_name}' \n")
                print("The suggestion books are: \n")
            else:
                print(j)
                recommended_books.append(j)

    ## Also append the books written by the same author
    other_books = get_books_same_author(book_name)

    all_recommendations = recommended_books + other_books

    recommended_books_final = []
    for book in all_recommendations:
        book_info = get_info(book)
        recommended_books_final.append(book_info)

    return recommended_books_final

# %%
import pickle
pickle.dump(model, open('./artifacts/model.pkl', 'wb'))
pickle.dump(books_final, open('./artifacts/books_final.pkl', 'wb'))
pickle.dump(book_pivot, open('./artifacts/book_pivot.pkl', 'wb'))
pickle.dump(book_ratings_summary, open('./artifacts/book_ratings_summary.pkl', 'wb'))



# %%
