# -*- coding: utf-8 -*-
"""\
This is a python port of "Goose" orignialy licensed to Gravity.com
under one or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.

Python port was written by Xavier Grangier for Recrutae

Gravity.com licenses this file
to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from HTMLParser import HTMLParser
from goose.text import innerTrim
from goose.parsers import Parser


class OutputFormatter(object):

    def __init__(self, config):
        self.top_node = None
        self.config = config
        self.stopwords_class = config.stopwords_class

    def get_language(self, article):
        """\
        Returns the language is by the article or
        the configuration language
        """
        # we don't want to force the target laguage
        # so we use the article.meta_lang
        if self.config.use_meta_language == True:
            if article.meta_lang:
                return article.meta_lang[:2]
        return self.config.target_language

    def get_top_node(self):
        return self.top_node

    def get_formatted_text(self, article):
        self.top_node = article.top_node
        self.remove_negativescores_nodes()
        self.links_to_text()
        self.replace_with_text()
        self.remove_fewwords_paragraphs(article)
        return self.convert_to_text()

    def convert_to_text(self):
        txts = []
        for node in list(self.get_top_node()):
            txt = Parser.getText(node)
            if txt:
                txt = HTMLParser().unescape(txt)
                txts.append(innerTrim(txt))
        return '\n\n'.join(txts)

    def links_to_text(self):
        """\
        cleans up and converts any nodes that
        should be considered text into text
        """
        Parser.stripTags(self.get_top_node(), 'a')

    def remove_negativescores_nodes(self):
        """\
        if there are elements inside our top node
        that have a negative gravity score,
        let's give em the boot
        """
        gravity_items = self.top_node.cssselect("*[gravityScore]")
        for item in gravity_items:
            score = int(item.attrib.get('gravityScore'), 0)
            if score < 1:
                item.getparent().remove(item)

    def replace_with_text(self):
        """\
        replace common tags with just
        text so we don't have any crazy formatting issues
        so replace <br>, <i>, <strong>, etc....
        with whatever text is inside them
        code : http://lxml.de/api/lxml.etree-module.html#strip_tags
        """
        Parser.stripTags(self.get_top_node(), 'b', 'strong', 'i', 'br', 'sup')

    def remove_fewwords_paragraphs(self, article):
        """\
        remove paragraphs that have less than x number of words,
        would indicate that it's some sort of link
        """
        all_nodes = Parser.getElementsByTags(self.get_top_node(), ['*'])  # .cssselect('*')
        all_nodes.reverse()
        for el in all_nodes:
            text = Parser.getText(el)
            stop_words = self.stopwords_class(language=self.get_language(article)).getStopWordCount(text)
            if stop_words.getStopWordCount() < 3 \
                and len(Parser.getElementsByTag(el, tag='object')) == 0 \
                and len(Parser.getElementsByTag(el, tag='embed')) == 0:
                Parser.remove(el)
            # TODO
            # check if it is in the right place
            else:
                trimmed = Parser.getText(el)
                if trimmed.startswith("(") and trimmed.endswith(")"):
                    Parser.remove(el)


class StandardOutputFormatter(OutputFormatter):
    pass
