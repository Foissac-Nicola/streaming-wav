from flask import (render_template, request, jsonify)
from streamapp import app

from helpers.sparqlHelper import SPARQLHelper


@app.route('/search', methods=['POST'])
def search():
    search_filters = request.form.to_dict()    
    keywords = search_filters.pop('keywords', None)

    query = { k:keywords.split() if v == 'true' else [] for (k,v) in search_filters.items() }
    query['rating'] = [] if search_filters['rating'] == '0' else [search_filters['rating']]

    sp = SPARQLHelper("./streamapp/static/media/bdd.xml")
    sp.exec_query(**query)

    r1 = {'titre': 'What Do You Mean?', 'artiste': 'Justin Bieber '}
    r2 = {'titre': 'Company', 'artiste': 'Justin Bieber '}
    results = [r1, r2]
    return jsonify(status=200, results=results)

@app.route('/')
@app.route('/index')
def index():
    return render_template('./index.html')