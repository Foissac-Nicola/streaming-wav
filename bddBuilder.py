#!/usr/bin/env python3
# coding = utf-8

from helpers.xmlHelper import XMLHelper as xml
from helpers.rdfHelper import RDFHelper as rdf
from helpers.xmpHelper import XMPHelper as xmp
import os

class BDDBuilder :


    @staticmethod
    def create_entry(graph,path=None):
        xmp_data = xmp.extract_xmp(path)
        rdf_data =xml.parse_xml(xmp_data)
        rdf_data['path'] = path
        rdf.add_sound(graph,**rdf_data)

    @staticmethod
    def make_bdd(path=None):
        #pathDB = os.getcwd() + path
        #Abs_path = os.path.dirname(pathDB)
        graphe = rdf.create_rdf()
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith(".wav"):
                    BDDBuilder.create_entry(graphe,os.path.join(root, name))
        rdf.save_graph(graphe,"./bdd.xml")

    @staticmethod
    def test(path=None):
        xmp_data = xmp.extract_xmp(path)
        # print(xmp_data)
        rdf_data =xml.parse_xml(xmp_data)
        g=rdf.create_rdf()
        rdf.add_sound(g,'',**rdf_data)



BDDBuilder.make_bdd(u".")