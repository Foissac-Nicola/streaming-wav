from flask import (render_template, request, jsonify)
from streamapp import app

@app.route('/search', methods=['POST'])
def search():
    search_filters = request.form.to_dict()
    print(search_filters)

    r1 = {'titre': 'What Do You Mean?', 'artiste': 'Justin Bieber '}
    r2 = {'titre': 'Company', 'artiste': 'Justin Bieber '}
    results = [r1, r2]
    return jsonify(status=200, results=results)

@app.route('/')
@app.route('/index')
def index():
    genre = get_genre()
    return render_template('./index.html', genre=genre)


def get_genre():
    return ["Tout", "Comédie Musicale", "Country", "Dance", "Death Métal", "Disco"]