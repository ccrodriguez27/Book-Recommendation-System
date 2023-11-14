# Book-Recommendation-System

https://github.com/ccrodriguez27/Book-Recommendation-System/assets/109123040/b011f603-c171-4c29-9769-641cac2e5b07

### About the project:
Collaborative filtering is a recommendation technique that predicts a user's preferences or interests by leveraging the collective behavior and preferences of a group of users. Instead of relying on explicit features of items or users, it assumes that users who agreed in the past tend to agree in the future. There are two main types of collaborative filtering:

1. User-Based Collaborative Filtering:
- Recommends items based on the preferences and behaviors of users who are similar to the target user.
- Identifies users with similar tastes and recommends items liked by similar users.

2. Item-Based Collaborative Filtering:
- Recommends items similar to those that a user has liked or interacted with in the past.
- Identifies items that are similar to the ones the user has shown interest in and recommends them.

This project implements user-based collaborative filtering.

#### Dataset Description: 
This project utilizes the following dataset: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset

It consists of three files - Books, Users, and Ratings. The "Books" dataset contains basic information on the book's title, author, publisher, year of publication, and ISBN. User demographic information can be found in the "Users" file, while the "Ratings" data contain user ratings given to each book, ranging from 0-10.

#### Methodology:
1. Filtering: Removed books and users with fewer than 30 ratings.

2. Matrix Construction: Created a user-item matrix using ratings as values.

3. Algorithm Application: Utilized the KNN algorithm to identify the most similar books, employing cosine similarity as the distance metric.



