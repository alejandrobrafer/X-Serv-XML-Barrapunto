#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        # Los datos de las páginas se encuentras tras la etiqueta 'item'.
        # Nota apararece otros 'link' y 'title' que no me interesa.
        if name == 'item':
            self.inItem = True
        elif self.inItem:
			# Esto en el contenido buscado cuando leo la etiqueta 'title' o 'link'.  
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
		# Salgo de '/item', luego ya no estoy en el contenido buscado.
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.line = self.theContent
                # To avoid Unicode trouble
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
				link = "<a href='" + self.theContent + "'>" + self.line + "</a><br>"
				print(link)
				self.inContent = False
				self.theContent = ""

    def characters (self, chars):
		# Si estoy en el contenido, añado a la varible inContent los caracteres.
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog
# Load parser and driver
print("HTTP/1.1 200 OK \r\n\r\n<html><body>")
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = urllib.urlopen('http://barrapunto.com/index.rss')
theParser.parse(xmlFile)
print("</body></html>")
