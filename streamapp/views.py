import socket, sys
from flask import (render_template, request, jsonify)
from streamapp import app

from helpers.sparqlHelper import SPARQLHelper


@app.route('/play', methods=['POST'])
def play():
    path = request.form['path']
    msg = "POST /play HTTP/1.1 200 \n\n" + path

    m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        m_socket.connect(("127.0.0.1", 7800))
        m_socket.send(msg.encode("Utf8"))
        m_socket.close()
    except socket.error as error:
        print("Play music failed - Error:", error)

    return jsonify(status=200)


@app.route('/search', methods=['POST'])
def search():
    search_filters = request.form.to_dict()    
    keywords = search_filters.pop('keywords', None)

    query = { k:keywords.split() if v == 'true' else [] for (k,v) in search_filters.items() }
    query['rating'] = [] if search_filters['rating'] == '0' else [search_filters['rating']]

    print('-------- QUERY SEND --------')
    print(query)

    sp = SPARQLHelper("./streamapp/static/media/bdd.xml")
    results = sp.exec_query(**query)
    
    return jsonify(status=200, results=results)

@app.route('/')
@app.route('/index')
def index():
    return render_template('./index.html')