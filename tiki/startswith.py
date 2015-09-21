#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib
import lxml.html
from lxml.cssselect import CSSSelector


class Startswith:
    """etc."""
    def __init__(self, message):
        self.__message = message
        self.__arrayParams = self.__getArrayParams()
        self.__stringParams = self.__getStringParams()

    def __getArrayParams(self):
        params = self.__message.split(' ')
        del params[0]

        return params

    def __getStringParams(self):
        params = self.__message.split(' ')
        command = params[0]

        return self.__message[len(command)+1:]

    def thimwiki(self):
        lang = 'vi'
        if '--lang' in self.__stringParams:
            langIdx = self.__stringParams.find('--lang')+7
            lang = self.__stringParams[langIdx:]
            self.__stringParams = self.__stringParams[:langIdx-7]

        query = self.__stringParams
        query = urllib.quote(query)

        url = "http://"+lang+".wikipedia.org/w/index.php?title=Special%3ASearch&profile=default&search="+query+"&fulltext=Search"
        resultPage = urllib.urlopen(url).read()
        print(resultPage)

        if "mw-search-nonefound" in resultPage:
            return "Thím hổng tìm ra gì trên Wiki cho cái này :("

        # build the DOM Tree
        tree = lxml.html.fromstring(resultPage)

        # construct a CSS Selector
        sel = CSSSelector('.mw-search-results>li:nth-child(1)')

        # Apply the selector to the DOM tree.
        results = sel(tree)
        # print the HTML for the first result.
        firstResult = results[0]
        sel2 = CSSSelector('li>div>a')

        a = sel2(firstResult)
        astr = lxml.html.tostring(a[0])

        href = re.search("(\"\/wiki\/)(.*?)\"",astr)
        gotoUrl = "http://"+lang+".wikipedia.org"+ href.group(0)[1:-1]
        return gotoUrl

    def abc(self):
        print(self.__getStringParams())
        return

