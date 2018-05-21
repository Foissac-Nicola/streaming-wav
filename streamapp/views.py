import socket, sys,uuid
from flask import (render_template, request, jsonify , session )
from streamapp import app
from streaming import RTPClient as rtp
from helpers.sparqlHelper import SPARQLHelper


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/play', methods=['POST'])
def play():
    check_uuid()
    client = rtp.RTPClient("127.0.0.1", 7800)
    client.send_play(request.form['path'],str(session["user_id"]))
    return jsonify(status=200)

@app.route('/pause', methods=['POST'])
def pause():
        check_uuid()
        client = rtp.RTPClient("127.0.0.1", 7800)
        client.send_pause(request.form['path'], str(session["user_id"]))
        return jsonify(status=200)

@app.route('/unpause', methods=['POST'])
def unpause():
        check_uuid()
        path = request.form['path']
        # todo implementation le server le fait a tester mardi

        return jsonify(status=200)

@app.route('/replay', methods=['POST'])
def replay():
        check_uuid()
        path = request.form['path']
        # todo implementation le server le fait a tester mardi

        return jsonify(status=200)

@app.route('/disconnect', methods=['POST'])
def disconnect():
        check_uuid()
        path = request.form['path']
        # todo implementation le server le fait a tester mardi

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


#5fdc50fc-5b4a-11e8-8f53-44850057d794
#8af9b504-5b4a-11e8-9383-44850057d794
