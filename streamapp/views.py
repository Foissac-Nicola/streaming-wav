import socket, sys,uuid
from flask import (render_template, request, jsonify , session)
from streamapp import app

from helpers.sparqlHelper import SPARQLHelper


@app.route('/play', methods=['POST'])
def play():
    check_uuid()
    path = request.form['path']
    msg = str("PLAY "+path+" RTP/1.0 200 " + str(session["user_id"]))
    print(msg)

    m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        m_socket.connect(("127.0.0.1", 7800))
        m_socket.send(msg.encode("Utf8"))
        m_socket.close()
    except socket.error as error:
        print("Play music failed - Error:", error)

    return jsonify(status=200)

@app.route('/pause', methods=['POST'])
def pause():
        check_uuid()
        path = request.form['path']
        msg = str("PAUSE " + path + " RTP/1.0 200 " + str(session["user_id"]))
        print(msg)

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
    check_uuid()
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
    check_uuid()
    return render_template('./index.html')

def check_uuid():
    if 'link' not in session :
        session["user_id"] = uuid.uuid1()
        session['link'] = True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#5fdc50fc-5b4a-11e8-8f53-44850057d794
#8af9b504-5b4a-11e8-9383-44850057d794
