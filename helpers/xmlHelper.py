#!/usr/bin/env python3
# coding = utf-8

from xml.dom.minidom import parseString as parseDocumentXml



class XMLHelper:
    """
        This class provide lot of method to find some rdf tag in xml file.
    """

    @staticmethod
    def find_rating(document):
        """
            This method find rating tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node list
        """
        nodelist = document.getElementsByTagName("xmp:Rating")
        if len(nodelist) > 0:
            return nodelist[0].firstChild.nodeValue
        return None

    @staticmethod
    def find_rights(document):
        """
            This method find rating tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node list
        """
        nodelist = document.getElementsByTagName("xmpRights:Marked")
        if len(nodelist) > 0:
            return nodelist[0].firstChild.nodeValue.lower()
        return None

    @staticmethod
    def find_instrument(document):
        """
            This method find rating tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node list
        """
        nodelist = document.getElementsByTagName("xmpDM:instrument")
        if len(nodelist) > 0:
            return nodelist[0].firstChild.nodeValue.lower().split(", ")
        return []

    @staticmethod
    def find_author(document):
        """
            This method find rating tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node list
        """
        nodelist = document.getElementsByTagName("xmpDM:artist")
        if len(nodelist) > 0:
            return nodelist[0].firstChild.nodeValue.lower()
        return None

    @staticmethod
    def find_date(document):
        """
            This method find rating tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node list
        """
        nodelist = document.getElementsByTagName("xmp:MetadataDate")
        if len(nodelist) > 0:
            return nodelist[0].firstChild.nodeValue
        return None


    @staticmethod
    def find_composer(document):
        """
            This method find rating tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node list
        """
        nodelist = document.getElementsByTagName("xmpDM:composer")
        if len(nodelist) > 0:
            return nodelist[0].firstChild.nodeValue.lower()
        return None

    @staticmethod
    def find_genre(document):
        """
            This method find genre tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node value
        """
        nodelist = document.getElementsByTagName("xmpDM:genre")
        if len(nodelist) > 0:
            return nodelist[0].firstChild.nodeValue.lower()
        return None


    @staticmethod
    def find_title(document):
        """
            This method find title tag in document
        :param document: xml(xmp) document
        :return: None if not found otherwise node list
        """
        nodelist = document.getElementsByTagName("dc:title")
        if len(nodelist) > 0:
            nodelist = nodelist[0].getElementsByTagName("rdf:Alt")
            if len(nodelist) > 0:
                nodelist=nodelist[0].getElementsByTagName("rdf:li")
                if(len(nodelist))>0:
                    return nodelist[0].firstChild.nodeValue.lower()
        return None

    @staticmethod
    def find_description(document):
        """
            This method find description tag in document
        :param document: xml(xmp) document
        :return: Emtpy list if not found otherwise list
        """
        nodelist = document.getElementsByTagName("dc:description")
        if len(nodelist) > 0:
            nodelist = nodelist[0].getElementsByTagName("rdf:Alt")
            if len(nodelist) > 0:
                nodelist=nodelist[0].getElementsByTagName("rdf:li")
                if(len(nodelist))>0:
                    return "".join(l for l in nodelist[0].firstChild.nodeValue.lower() if l not in ['.']).split(" ")
        return []

    @staticmethod
    def find_subject(document):
        """
            This method find subject tag in document
        :param document: xml(xmp) document
        :return: Emtpy list if not found otherwise list
        """
        ret = []
        nodelist = document.getElementsByTagName("dc:subject")
        if len(nodelist) > 0:
            nodelist = nodelist[0].getElementsByTagName("rdf:Bag")
            if len(nodelist) > 0:
                nodelist=nodelist[0].getElementsByTagName("rdf:li")
                if(len(nodelist))>0:
                    for item in nodelist :
                        ret.append(item.firstChild.nodeValue.lower())
                    return ret
        return ret

    @staticmethod
    def parse_xml(xml):
        """
            This method parse all tag for rdf helper
        :param xml:
        :return: dict of tag
        """
        ret = {}
        doc = parseDocumentXml(xml)
        ret['instrument'] = XMLHelper.find_instrument(doc)
        ret['subject'] = XMLHelper.find_subject(doc)
        ret['description']= XMLHelper.find_description(doc)
        ret['title'] = XMLHelper.find_title(doc)
        ret['author'] = XMLHelper.find_author(doc)
        ret['composer'] = XMLHelper.find_composer(doc)
        ret['date'] = XMLHelper.find_date(doc)
        ret['genre'] = XMLHelper.find_genre(doc)
        ret['rating'] = XMLHelper.find_rating(doc)
        ret['rigth'] = XMLHelper.find_rights(doc)
        return ret