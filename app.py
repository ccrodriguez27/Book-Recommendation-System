# %%
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from utils import books_final, recommend_books, get_info

# %% 
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

all_books = books_final['Book-Title'].tolist()

# %%
app.layout = html.Div([
    html.H1("Book Recommendation System", style={'margin-top': '20px', 'margin-left': '20px'}),  # Add margin-top to the title
    
    html.H6("Select a book:", style = {'margin-top': '20px', 'margin-left': '20px'}),
    dcc.Dropdown(
        id='book-dropdown',
        options=[{'label': book, 'value': book} for book in all_books],
        value=None,
        placeholder="Book Title",
        style={'width': '80%', 'margin-top': '10px', 'margin-left': '10px'}  # Add margin-left for space
    ),
    
    dbc.Button('Get Suggestions', id='get-suggestions-button', style={'margin-top': '20px', 'margin-left': '20px'}),  # Add margin-top and margin-left
    
    html.Div(id='suggestions-output', style={'display': 'flex', 'flexWrap': 'wrap', 'alignItems': 'center', 'margin': '20px'})
])
#%%
@app.callback(
    Output('suggestions-output', 'children'),
    [Input('get-suggestions-button', 'n_clicks')],
    State('book-dropdown', 'value')
)
def get_suggestions(n_clicks, selected_book):
    if n_clicks is None:
        return ''
    selected_book_info = [get_info(selected_book)]

    suggestions = recommend_books(selected_book)
    all_books = selected_book_info + suggestions
    # Format the suggestions as HTML
    suggestions_html = [
        html.Div([
            html.Img(src=book['Image-URL-L'], style={'width': '100px', 'height': '150px', 'margin': 'auto', 'display': 'block'}),
            html.P(book['Book-Title'], style={'font-weight': 'bold', 'margin-top': '20px','font-size': '18px'}),
            html.P(f"Author: {book['Book-Author']}"),
            html.P(f"Year of Publication: {book['Year-Of-Publication']}"),
            html.P(f"Publisher: {book['Publisher']}"),
            html.P(f"Average Rating: {book['Average Rating']}/10"),
            #html.P(f"Median Rating: {book['Median Rating']}/10"),
            html.P(f"Rating Count: {book['Rating Count']}")
        ],
        style={'text-align': 'left', 'margin': '20px', 'width': '12%'})
        for book in all_books
    ]

    return suggestions_html

if __name__ == '__main__':
    app.run_server(debug=False)

# %%
