#!/usr/bin/env python3
# coding = utf-8

import rdflib as rdf


class RDFHelper:

    @staticmethod
    def create_rdf():
        return rdf.Graph()

    @staticmethod
    def add_sound_rating(graph,sound,rating=None):
        if rating is not None:
            node_rating= rdf.URIRef(u'urn:/streaming/rating')
            graph.add((sound, node_rating, rdf.Literal(rating)))
        return graph

    @staticmethod
    def add_sound_author(graph,sound,author=None):
        if author is not None:
            node_author = rdf.URIRef(u'urn:/streaming/author')
            graph.add((sound, node_author, rdf.Literal(author)))
        return graph

    @staticmethod
    def add_sound_composer(graph,sound,composer=None):
        if composer is not None:
            node_composer = rdf.URIRef(u'urn:/streaming/composer')
            graph.add((sound, node_composer, rdf.Literal(composer)))
        return graph

    @staticmethod
    def add_sound_title(graph,sound,title=None):
        if title is not None:
            node_title = rdf.URIRef(u'urn:/streaming/title')
            graph.add((sound, node_title, rdf.Literal(title)))
        return graph

    @staticmethod
    def add_sound_path(graph,sound,path=None):
        if path is not None:
            node_path = rdf.URIRef(u'urn:/streaming/path')
            graph.add((sound, node_path, rdf.Literal(path)))
        return graph

    @staticmethod
    def add_sound_date(graph,sound,date=None):
        if date is not None:
            node_date = rdf.URIRef(u'urn:/streaming/date_creation')
            graph.add((sound, node_date, rdf.Literal(date)))
        return graph

    @staticmethod
    def add_sound_genre(graph,sound,genre=None):
        if genre is not None:
            node_genre = rdf.URIRef(u'urn:/streaming/genre')
            graph.add((sound, node_genre, rdf.Literal(genre)))
        return graph

    @staticmethod
    def add_sound_right(graph,sound,rigth=None):
        if rigth is not None:
            node_rigth = rdf.URIRef(u'urn:/streaming/rigth')
            graph.add((sound, node_rigth, rdf.Literal(rigth)))
        return graph

    @staticmethod
    def add_sound_instrument(graph,sound,instrument=[]):
        if len(instrument) > 0:
            bnode_instruments = rdf.BNode()
            node_instrument = rdf.URIRef(u'urn:/streaming/instrument')
            graph.add((sound, node_instrument, bnode_instruments))
            for entry in instrument:
                graph.add((bnode_instruments, rdf.RDF.li, rdf.Literal(entry)))
        return graph

    @staticmethod
    def add_sound_subject(graph,sound,subject=[]):
        if len(subject) > 0:
            bnode_subjects = rdf.BNode()
            node_subject = rdf.URIRef(u'urn:/streaming/subject')
            graph.add((sound, node_subject, bnode_subjects))
            for entry in subject:
                graph.add((bnode_subjects, rdf.RDF.li, rdf.Literal(entry)))
        return graph

    @staticmethod
    def add_sound_comment(graph,sound,description=[]):
        if len(description) > 0:
            bnode_comments = rdf.BNode()
            node_comment= rdf.URIRef(u'urn:/streaming/comment')
            graph.add((sound, node_comment, bnode_comments))
            for entry in description:
                graph.add((bnode_comments, rdf.RDF.li, rdf.Literal(entry)))
        return graph


    @staticmethod
    def add_sound(graph,path=None,title=None,author=None,composer=None,genre=None,rating=None,date=None,rigth=None,instrument=[],description=[],subject=[]):

        k = rdf.Namespace(u"urn:/streaming/")
        bnode_sound = rdf.BNode()
        graph=RDFHelper.add_sound_path(graph,bnode_sound,path=path)
        graph=RDFHelper.add_sound_title(graph,bnode_sound,title=title)
        graph=RDFHelper.add_sound_author(graph,bnode_sound,author=author)
        graph=RDFHelper.add_sound_composer(graph,bnode_sound,composer=composer)
        graph=RDFHelper.add_sound_genre(graph, bnode_sound,genre=genre)
        graph=RDFHelper.add_sound_rating(graph,bnode_sound,rating=rating)
        graph=RDFHelper.add_sound_date(graph,bnode_sound,date=date)
        graph=RDFHelper.add_sound_right(graph, bnode_sound,rigth=rigth)
        graph=RDFHelper.add_sound_instrument(graph,bnode_sound,instrument=instrument)
        graph=RDFHelper.add_sound_subject(graph, bnode_sound, subject=subject)
        graph=RDFHelper.add_sound_comment(graph, bnode_sound, description=description)
        graph.bind("strm", k)

    @staticmethod
    def save_graph(graph,path):
        k = rdf.Namespace(u"urn:/streaming/")
        graph.bind("strm", k)
        file = open(path, "wb")
        file.write(graph.serialize(format='xml'))
        file.close()
        return graph





