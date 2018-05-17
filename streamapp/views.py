from flask import (render_template, jsonify)
from streamapp import app

@app.route('/search', methods=['POST'])
def search():
    
    return jsonify(status=200)

@app.route('/')
@app.route('/index')
def index():
    genre = get_genre()
    return render_template('./index.html', genre=genre)


def get_genre():
    return ["Tout", "Comédie Musicale", "Country", "Dance", "Death Métal", "Disco"]