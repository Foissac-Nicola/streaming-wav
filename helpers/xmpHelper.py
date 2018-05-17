#!/usr/bin/env python3
# coding = utf-8
import libxmp


class XMPHelper:
     @staticmethod
     def extract_xmp(file_path, open_forupdate=False):
        xmpfile = libxmp.XMPFiles(file_path=file_path, open_forupdate=open_forupdate)
        libxmp.XMPFiles()
        xmp = xmpfile.get_xmp()
        xmpfile.close_file()
        return xmp.serialize_to_unicode()