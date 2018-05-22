#!/usr/bin/env python3
# coding = utf-8
import libxmp


class XMPHelper:
    """
        This class provide extract xmp for dumping xmp of file.
    """
    @staticmethod
    def extract_xmp(file_path, open_forupdate=False):
        """
            This method use xmp lib to extra xmp metadata
        :param file_path: path
        :param open_forupdate: False by default
        :return: unicode string representation of xmp metadata
        """
        xmpfile = libxmp.XMPFiles(file_path=file_path, open_forupdate=open_forupdate)
        libxmp.XMPFiles()
        xmp = xmpfile.get_xmp()
        xmpfile.close_file()
        return xmp.serialize_to_unicode()