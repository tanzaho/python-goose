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
from goose.utils import ReplaceSequence
from lxml.html import clean
from urlparse import urlsplit
from goose.text import innerTrim
from configuration import Configuration
from host_utils import HostUtils

KNOWN_HOST_REMOVE_SELECTORS = {
    'www.ebay.com': '#desc_div, [class *= "drpdwn"], .dropdownmenu, #PaginationAndExpansionsContainer, #ConstraintCaptionContainer, .noImage div, .yesImage div, .yesImage img[src *= "://ir"], .yesVideo, [class ^= addCaption], .removeModalLayer',
    'www.goal.com': '[href="http://www.adobe.com/go/getflashplayer"], .hidden',
    'www.linkedin.com': '.item-actions',
    'twitpic.com': '#media-stats, #media-comments',
    'www.twitpic.com': { 'reference': 'twitpic.com' },
    'slickdeals.net': '.buynow',
    'ask.fm': '.likeCombo, .like-face-container, .time',
    'stackoverflow.com': '[itemprop="answerCount"], .reputation-score, .badgecount, .relativetime',
    'cooking.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'serverfault.com': { 'reference': 'stackoverflow.com' },
    'superuser.com': { 'reference': 'stackoverflow.com' },
    'webapps.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'askubuntu.com': { 'reference': 'stackoverflow.com' },
    'webmasters.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'gamedev.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'tex.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'programmers.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'unix.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'apple.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'wordpress.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'gis.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'electronics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'android.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'security.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'dba.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'drupal.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'sharepoint.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'ux.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'mathematica.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'salesforce.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'raspberrypi.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'magento.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'pt.stackoverflow.com': { 'reference': 'stackoverflow.com' },
    'blender.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'networkengineering.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'meta.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'windowsphone.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'sqa.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'dsp.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'ja.stackoverflow.com': { 'reference': 'stackoverflow.com' },
    'arduino.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'crypto.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'softwarerecs.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'sound.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'codegolf.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'tor.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'joomla.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'reverseengineering.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'space.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'robotics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'expressionengine.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'emacs.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'craftcms.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'opendata.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'ebooks.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'datascience.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'tridion.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'engineering.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'gaming.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'photo.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'stats.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'math.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'diy.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'money.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'english.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'stackapps.com': { 'reference': 'stackoverflow.com' },
    'cstheory.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'rpg.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'bicycles.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'boardgames.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'physics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'homebrew.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'writers.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'video.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'graphicdesign.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'scifi.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'codereview.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'quant.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'pm.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'skeptics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'fitness.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'mechanics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'parenting.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'music.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'judaism.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'german.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'japanese.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'philosophy.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'gardening.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'travel.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'productivity.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'french.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'christianity.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'bitcoin.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'linguistics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'hermeneutics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'history.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'bricks.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'spanish.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'scicomp.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'movies.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'chinese.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'biology.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'poker.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'cogsci.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'outdoors.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'martialarts.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'sports.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'academia.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'cs.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'workplace.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'chemistry.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'chess.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'russian.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'islam.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'patents.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'genealogy.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'politics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'anime.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'ell.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'sustainability.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'freelancing.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'mathoverflow.net': { 'reference': 'stackoverflow.com' },
    'astronomy.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'pets.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'ham.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'italian.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'aviation.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'beer.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'expatriates.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'matheducators.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'earthscience.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'puzzling.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'buddhism.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'hinduism.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'communitybuilding.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'startups.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'worldbuilding.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'hsm.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'economics.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'lifehacks.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'coffee.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'vi.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'musicfans.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'woodworking.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'civicrm.stackexchange.com': { 'reference': 'stackoverflow.com' },
    'ru.stackoverflow.com': { 'reference': 'stackoverflow.com' },
}

class OutputFormatterCleaner(clean.Cleaner):
    config = Configuration()
    parser = config.get_parser()
    safe_attrs_only = True
    host_whitelist = ['www.youtube.com', 'player.vimeo.com', 'w.soundcloud.com',
                      'embed.spotify.com']

    def __init__(self, **kw):
        super(OutputFormatterCleaner, **kw)
        self.safe_attrs = self.__safe_attrs()

    def allow_embedded_url(self, el, url):
        if (self.whitelist_tags is not None
            and el.tag not in self.whitelist_tags):
            return False
        scheme, netloc, path, query, fragment = urlsplit(url)
        netloc = netloc.lower().split(':', 1)[0]
        if scheme not in ('http', 'https', ''):
            return False
        if netloc in self.host_whitelist:
            return True
        return False

    def clean(self, node):
        html_string = self.parser.nodeToString(node, method='html')
        clean_html_string = self.clean_html(html_string)
        return innerTrim(clean_html_string)

    def __safe_attrs(self):
        attributes = set(clean.defs.safe_attrs)
        for remove_attribute in ['class', 'id', 'tabindex']:
            attributes.remove(remove_attribute)
        return attributes


class DocumentCleaner(object):

    def __init__(self, config, article):
        # config
        self.config = config

        # parser
        self.parser = self.config.get_parser()

        # article
        self.article = article

        # nodes to remove regexp
        self.remove_nodes_re = (
        "^side$|combx|retweet|mediaarticlerelated|menucontainer|"
        "navbar|storytopbar-bucket|utility-bar|inline-share-tools"
        "|comment|PopularQuestions|contact|foot|footer|Footer|footnote"
        "|cnn_strycaptiontxt|cnn_html_slideshow|cnn_strylftcntnt"
        "|^links$|meta$|shoutbox|sponsor"
        "|tags|socialnetworking|socialNetworking|cnnStryHghLght"
        "|cnn_stryspcvbx|^inset$|pagetools|post-attributes"
        "|welcome_form|contentTools2|the_answers"
        "|communitypromo|runaroundLeft|subscribe|vcard|articleheadings"
        "|date|^print$|popup|author-dropdown|tools|socialtools|byline"
        "|konafilter|KonaFilter|breadcrumbs|^fn$|wp-caption-text"
        "|legende|ajoutVideo|timestamp|js_replies|printfriendly|share"
        )

        # dailymail remove nodes
        self.remove_nodes_re += "|related-carousel|xwv-related-videos-container"

        # nytimes remove nodes
        self.remove_nodes_re += "|visually-hidden|robots-nocontent"

        # *.wikipedia.org
        self.remove_nodes_re += "|mw-editsection|^cite_ref|noprint|References|siteSub"
        self.remove_nodes_re += "|collapsed|mw-headline-anchor|filetoc|noviewer"

        # *.wiktionary.org
        self.remove_nodes_re += "|ib-brac"

        # *.wikibooks.org
        self.remove_nodes_re += "|status-icon"

        # www.wikidata.org
        self.remove_nodes_re += "|wikibase-edittoolbar-container"

        # http://www.dailymail.co.uk/news/article-2742786/Complacent-Home-Office-loses-175-000-illegal-immigrants-Fresh-humiliation-officials-admit-went-missing-refused-permission-stay.html
        self.remove_nodes_re += "|most-read-news-wrapper|most-watched-videos-wrapper"

        self.regexp_namespace = "http://exslt.org/regular-expressions"
        self.nauthy_ids_re = "//*[re:test(@id, '%s', 'i')]" % self.remove_nodes_re
        self.nauthy_classes_re = "//*[re:test(@class, '%s', 'i')]" % self.remove_nodes_re
        self.nauthy_names_re = "//*[re:test(@name, '%s', 'i')]" % self.remove_nodes_re
        self.nauthy_tags = ["noscript"]
        self.google_re = " google "
        self.entries_re = "^[^entry-]more.*$"
        self.facebook_re = "[^-]facebook"
        self.facebook_braodcasting_re = "facebook-broadcasting"
        self.twitter_re = "[^-]twitter"
        self.tablines_replacements = ReplaceSequence()\
                                            .create("\n", "\n\n")\
                                            .append("\t")\
                                            .append("^\\s+$")

    def clean(self):
        doc_to_clean = self.article.doc
        doc_to_clean = self.remove_scripts_styles(doc_to_clean)
        if self.article.domain in KNOWN_HOST_REMOVE_SELECTORS:
            return self.remove_host_specific_nodes(doc_to_clean)
        doc_to_clean = self.clean_body_classes(doc_to_clean)
        doc_to_clean = self.clean_article_tags(doc_to_clean)
        doc_to_clean = self.remove_drop_caps(doc_to_clean)
        doc_to_clean = self.clean_bad_tags(doc_to_clean)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.google_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.entries_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.facebook_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.facebook_braodcasting_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.twitter_re)
        doc_to_clean = self.clean_para_spans(doc_to_clean)
        doc_to_clean = self.div_to_para(doc_to_clean, 'div')
        doc_to_clean = self.div_to_para(doc_to_clean, 'span')
        return doc_to_clean

    def clean_body_classes(self, doc):
        # we don't need body classes
        # in case it matches an unwanted class all the document
        # will be empty
        elements = self.parser.getElementsByTag(doc, tag="body")
        if elements:
            self.parser.delAttribute(elements[0], attr="class")
        return doc

    def clean_article_tags(self, doc):
        articles = self.parser.getElementsByTag(doc, tag='article')
        for article in articles:
            for attr in ['id', 'name', 'class']:
                self.parser.delAttribute(article, attr=attr)
        return doc

    def remove_drop_caps(self, doc):
        items = self.parser.css_select(doc, "span[class~=dropcap], span[class~=drop_cap]")
        for item in items:
            self.parser.drop_tag(item)

        return doc

    def remove_scripts_styles(self, doc):
        # remove scripts
        scripts = self.parser.getElementsByTag(doc, tag='script')
        for item in scripts:
            self.parser.remove(item)

        # remove styles
        styles = self.parser.getElementsByTag(doc, tag='style')
        for item in styles:
            self.parser.remove(item)

        # remove comments
        comments = self.parser.getComments(doc)
        for item in comments:
            self.parser.remove(item)

        return doc

    def clean_bad_tags(self, doc):
        # ids
        naughty_list = self.parser.xpath_re(doc, self.nauthy_ids_re)
        for node in naughty_list:
            self.parser.remove(node)

        # class
        naughty_classes = self.parser.xpath_re(doc, self.nauthy_classes_re)
        for node in naughty_classes:
            self.parser.remove(node)

        # name
        naughty_names = self.parser.xpath_re(doc, self.nauthy_names_re)
        for node in naughty_names:
            self.parser.remove(node)

        for nauthy_tag in self.nauthy_tags:
            nodes = self.parser.getElementsByTag(doc, tag=nauthy_tag)
            for node in nodes:
                images = self.parser.getElementsByTag(node, tag='img')
                if images:
                    parent = node.getparent()
                    parent_index = parent.index(node)
                    for image in images:
                        parent.insert(parent_index, image)
                else:
                    self.parser.remove(node)

        return doc

    def remove_host_specific_nodes(self, doc):
        remove_selectors = HostUtils.host_selectors(KNOWN_HOST_REMOVE_SELECTORS, self.article.domain)
        nodes = self.parser.css_select(doc, remove_selectors)
        for node in nodes:
            self.parser.remove(node)

        return doc

    def remove_nodes_regex(self, doc, pattern):
        for selector in ['id', 'class']:
            reg = "//*[re:test(@%s, '%s', 'i')]" % (selector, pattern)
            naughty_list = self.parser.xpath_re(doc, reg)
            for node in naughty_list:
                self.parser.remove(node)
        return doc

    def clean_para_spans(self, doc):
        spans = self.parser.css_select(doc, 'p span')
        for item in spans:
            self.parser.drop_tag(item)
        return doc

    def get_flushed_buffer(self, replacement_text, doc):
        return self.parser.textToPara(replacement_text)

    def get_replacement_nodes(self, doc, div):
        replacement_text = []
        nodes_to_return = []
        nodes_to_remove = []
        childs = self.parser.childNodesWithText(div)

        for kid in childs:
            # node is a p
            # and already have some replacement text
            if self.parser.getTag(kid) == 'p' and len(replacement_text) > 0:
                newNode = self.get_flushed_buffer(''.join(replacement_text), doc)
                nodes_to_return.append(newNode)
                replacement_text = []
                nodes_to_return.append(kid)
            # node is a text node
            elif self.parser.isTextNode(kid):
                kid_text_node = kid
                kid_text = self.parser.getText(kid)
                replace_text = self.tablines_replacements.replaceAll(kid_text)
                if(len(replace_text)) > 1:
                    previous_sibling_node = self.parser.previousSibling(kid_text_node)
                    while previous_sibling_node is not None \
                        and self.parser.getTag(previous_sibling_node) == "a" \
                        and self.parser.getAttribute(previous_sibling_node, 'grv-usedalready') != 'yes':
                        outer = " " + self.parser.outerHtml(previous_sibling_node) + " "
                        replacement_text.append(outer)
                        nodes_to_remove.append(previous_sibling_node)
                        self.parser.setAttribute(previous_sibling_node,
                                    attr='grv-usedalready', value='yes')
                        prev = self.parser.previousSibling(previous_sibling_node)
                        previous_sibling_node = prev if prev is not None else None
                    next_sibling_node = self.parser.nextSibling(kid_text_node)
                    while next_sibling_node is not None \
                        and self.parser.getTag(next_sibling_node) == "a" \
                        and self.parser.getAttribute(next_sibling_node, 'grv-usedalready') != 'yes':
                        outer = " " + self.parser.outerHtml(next_sibling_node) + " "
                        replacement_text.append(outer)
                        nodes_to_remove.append(next_sibling_node)
                        self.parser.setAttribute(next_sibling_node,
                                    attr='grv-usedalready', value='yes')
                        next = self.parser.nextSibling(next_sibling_node)
                        previous_sibling_node = next if next is not None else None

            # otherwise
            else:
                nodes_to_return.append(kid)

        # flush out anything still remaining
        if(len(replacement_text) > 0):
            new_node = self.get_flushed_buffer(''.join(replacement_text), doc)
            nodes_to_return.append(new_node)
            replacement_text = []

        for n in nodes_to_remove:
            self.parser.remove(n)

        return nodes_to_return

    def replace_with_para(self, doc, div):
        self.parser.replaceTag(div, 'p')

    def div_to_para(self, doc, dom_type):
        bad_divs = 0
        else_divs = 0
        divs = self.parser.getElementsByTag(doc, tag=dom_type)
        tags = ['a', 'blockquote', 'dl', 'div', 'img', 'ol', 'p', 'pre', 'table', 'ul']

        for div in divs:
            items = self.parser.getElementsByTags(div, tags)
            if div is not None and len(items) == 0:
                self.replace_with_para(doc, div)
                bad_divs += 1
            elif div is not None:
                replaceNodes = self.get_replacement_nodes(doc, div)
                for child in self.parser.childNodes(div):
                    div.remove(child)

                for c, n in enumerate(replaceNodes):
                    div.insert(c, n)

                else_divs += 1

        return doc


class StandardDocumentCleaner(DocumentCleaner):
    pass
