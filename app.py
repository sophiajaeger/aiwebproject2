print("Loading app.py")
from flask import Flask, request, render_template
from crawler import search # import search function from crawler.py 
# from testerei import search

app = Flask(__name__) # create instance of Flask app

@app.route('/') # define home route ("/")
def home():
    # diplay a basic search form
    return '''
    <h1>Search Engine:</h1>
    <form action="/search" method="get">
        <input type="text" name="q" placeholder="Search for words" required>
        <button type="submit">Search</button>
    </form>
    '''

@app.route('/search') # define the search rout ("/search")
def search_route():
    query = request.args.get('q')  # get search query from URL parameters
    if query:
        results, suggestions = search(query)  # pass to search function (crawler.py)
        return render_template('results.html', results=results, suggestions = suggestions)  # pas results to HTML tamplate
    return 'No query!'

# run the app in debug mode if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)

