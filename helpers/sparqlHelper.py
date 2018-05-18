#!/usr/bin/env python3
# coding = utf-8

import rdflib as rdf

class SPARQLHelper:

    def __init__(self,path) -> None:
        self.__graph = rdf.Graph()
        self.__graph.parse(path)

    def exec_query(self,**kwargs):
        self.__build_query(**kwargs)

        print(self.__query)
        qres = self.__graph.query(self.__query)

        if qres is not None:
            for row in qres:
                print(row)

    def __build_query(self,instrument=[], subject=[],description=[], title=[], author=[], composer=[], genre=[], rating=[], rigth=[]):
        self.__query = '''PREFIX strm: <urn:/streaming/>
         SELECT ?node ?title ?author ?path ?genre
         WHERE {
         ?node strm:subject [?li ?subject].
         ?node strm:comment [?li ?description].
         ?node strm:title ?title.
         ?node strm:author ?author.
         ?node strm:composer ?composer.
         ?node strm:genre ?genre.
         ?node strm:path ?path  
         '''
        self.__query = self.__query + '?node strm:instrument [?li ?instrument ].' if len(instrument) > 0 else self.__query + 'OPTIONAL { ?node strm:instrument [?li ?instrument ] }. '
        self.__query = self.__query + '?node strm:rating ?rating' if len(rating) > 0 else self.__query + 'OPTIONAL { ?node strm:rating ?rating } '
        if len(instrument) > 0 or len(subject) > 0 or len(description) or len(title) > 0 or len(author) > 0 or len(composer) > 0 or len(genre) > 0 or len(rating) :
            self.__query = self.__query + '. filter('
            self.__seek_instrument(instrument=instrument)
            self.__seek_subject(subject=subject)
            self.__seek_description(description=description)
            self.__seek_title(title=title)
            self.__seek_author(author=author)
            self.__seek_composer(composer=composer)
            self.__seek_genre(genre=genre)
            self.__seek_rating(rating=rating)
            self.__query = self.__query[:-4] + ')'

        self.__query = self.__query + '} group by ?node'

    def __seek_instrument(self,instrument=[]):
        for item in instrument :
            self.__query = self.__query + """?instrument = '"""+ item + """' || """

    def __seek_subject(self,subject=[]):
        for item in subject :
            self.__query = self.__query + """?subject = '"""+ item + """' || """

    def __seek_description(self,description=[]):
        for item in description :
            self.__query = self.__query + """?description = '"""+ item + """' || """

    def __seek_title(self,title=[]):
        for item in title :
            self.__query = self.__query + """?title = '"""+ item + """' || """

    def __seek_author(self,author=[]):
        for item in author :
            self.__query = self.__query + """?author = '"""+ item + """' || """

    def __seek_composer(self,composer=[]):
        for item in composer :
            self.__query = self.__query + """?composer = '"""+ item + """' || """

    def __seek_genre(self,genre=[]):
        for item in genre :
            self.__query = self.__query + """?genre = '"""+ item + """' || """

    def __seek_rating(self,rating=[]):
        for item in rating :
            self.__query = self.__query + """?rating = '"""+ item + """' || """



a = SPARQLHelper("testfile.xml")
t = {'genre': [], 'title': ['piano', 'doux'], 'author': [], 'composer': [], 'instrument': [], 'subject': [], 'description': ['piano', 'doux'], 'rating': ['5']}
a.exec_query(**t)
