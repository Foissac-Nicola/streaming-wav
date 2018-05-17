#!/usr/bin/env python3
# coding = utf-8
import libxmp
import sys


class XMPHelper:
     @staticmethod
     def extract_xmp(file_path, open_forupdate=False):
        xmpfile = libxmp.XMPFiles(file_path=file_path, open_forupdate=open_forupdate)
        libxmp.XMPFiles()
        xmp = xmpfile.get_xmp()
        xmpfile.close_file()
        print('XMP metadata = ', xmp)
        return xmp


XMPHelper.extract_xmp("./beta.wav")
XMPHelper.extract_xmp("./delta.wav")

# for arg in sys.argv:
#     # Read file
#     xmpfile = libxmp.XMPFiles(file_path=arg, open_forupdate=False)
#
#     # Get XMP from file
#     xmp = xmpfile.get_xmp()
#     print('XMP metadata = ', xmp)
#
#     xmpfile.close_file()
