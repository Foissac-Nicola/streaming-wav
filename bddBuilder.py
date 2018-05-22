#!/usr/bin/env python3
# coding = utf-8

from helpers.xmlHelper import XMLHelper as xml
from helpers.rdfHelper import RDFHelper as rdf
from helpers.xmpHelper import XMPHelper as xmp
import os
import sys

class BDDBuilder :

    @staticmethod
    def create_entry(graph,path=None):
        """
            This method create entry for bdd
        :param graph: rdf graph
        :param path: path of wav file
        :return: None
        """
        xmp_data = xmp.extract_xmp(path)
        rdf_data =xml.parse_xml(xmp_data)
        rdf_data['path'] = path
        rdf.add_sound(graph,**rdf_data)

    @staticmethod
    def make_bdd(path=None):
        """
            This method parse all file and dir in dir path whit wav extension
        :param path: dir of save bdd.xml file
        :return: None
        """
        graphe = rdf.create_rdf()
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith(".wav"):
                    BDDBuilder.create_entry(graphe,os.path.join(root, name))
        rdf.save_graph(graphe,"./bdd.xml")

if __name__ == '__main__':

    if len(sys.argv) >= 2:
        BDDBuilder.make_bdd(sys.argv[1])
    else:
        BDDBuilder.make_bdd(u".")