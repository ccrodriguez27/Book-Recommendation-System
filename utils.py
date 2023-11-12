# %%
import numpy as np
import pickle

# Specify the paths to your pkl files
model_path = './artifacts/model.pkl'
books_final_path = './artifacts/books_final.pkl'
book_pivot_path = './artifacts/book_pivot.pkl'
book_ratings_summary_path = './artifacts/book_ratings_summary.pkl'

# Load the pickled objects
model = pickle.load(open(model_path, 'rb'))
books_final = pickle.load(open(books_final_path, 'rb'))
book_pivot = pickle.load(open(book_pivot_path, 'rb'))
book_ratings_summary = pickle.load(open(book_ratings_summary_path, 'rb'))

# %%
def get_info(book_name):
    subset = books_final[books_final['Book-Title'] == book_name]
    subset = subset.reset_index(drop=True)
    info_dict = dict(subset.iloc[0])  # Convert the first row to a dictionary
    
    rating_count = book_ratings_summary[book_ratings_summary.index == info_dict['ISBN']]['Rating-Count'].values[0]
    average_rating = book_ratings_summary[book_ratings_summary.index == info_dict['ISBN']]['Average-Rating'].values[0]
    average_rating = np.round(average_rating, 1)

    median_rating = book_ratings_summary[book_ratings_summary.index == info_dict['ISBN']]['Median-Rating'].values[0]
    median_rating = np.round(median_rating, 1)

    info_dict['Rating Count'] = rating_count
    info_dict['Average Rating'] = average_rating
    info_dict['Median Rating'] = median_rating

    return info_dict

# %%
def get_books_same_author(book_name):
    author = books_final.loc[books_final['Book-Title'] == book_name, 'Book-Author'].reset_index(drop=True)[0]
    other_books = books_final.loc[books_final['Book-Author'] == author, 'Book-Title']

    
    other_books_by_author = list(other_books)
    other_books_by_author.remove(book_name)
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

    #all_recommendations = recommended_books + other_books
    all_recommendations = recommended_books
    recommended_books_final = []
    for book in all_recommendations:
        book_info = get_info(book)
        recommended_books_final.append(book_info)

    print(recommended_books_final)
    return recommended_books_final
# %%
