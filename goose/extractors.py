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
import re
from copy import deepcopy
from urlparse import urlparse, urljoin
from goose.utils import StringSplitter
from goose.utils import StringReplacement
from goose.utils import ReplaceSequence
from host_utils import HostUtils

MOTLEY_REPLACEMENT = StringReplacement("&#65533;", "")
ESCAPED_FRAGMENT_REPLACEMENT = StringReplacement(u"#!", u"?_escaped_fragment_=")
TITLE_REPLACEMENTS = ReplaceSequence().create(u"&raquo;").append(u"»")
TITLE_SPLITTERS = [u"|", u"-", u"»", u":"]
PIPE_SPLITTER = StringSplitter("\\|")
DASH_SPLITTER = StringSplitter(" - ")
ARROWS_SPLITTER = StringSplitter("»")
COLON_SPLITTER = StringSplitter(":")
SPACE_SPLITTER = StringSplitter(' ')
NO_STRINGS = set()
A_REL_TAG_SELECTOR = "a[rel=tag]"
A_HREF_TAG_SELECTOR = "a[href*='/tag/'], a[href*='/tags/'], a[href*='/topic/'], a[href*='?keyword=']"
RE_LANG = r'^[A-Za-z]{2}$'
KNOWN_PUBLISH_DATE_META_TAGS = [
    {'attribute': 'property', 'value': 'rnews:datePublished'},
    {'attribute': 'property', 'value': 'article:published_time'},
    {'attribute': 'name', 'value': 'OriginalPublicationDate'},
    {'attribute': 'itemprop', 'value': 'datePublished'},
    {'attribute': 'property', 'value': 'article:published'},
]
KNOWN_DESCRIPTION_META_TAGS = [
    {'attribute': 'name', 'value': 'description'},
    {'attribute': 'property', 'value': 'og:description'},
    {'attribute': 'property', 'value': 'rnews:description'},
    {'attribute': 'name', 'value': 'Description'}
]
KNOWN_CONTENT_TAGS = [
    {'attr': 'id', 'value': 'story-body'},
    {'attr': 'class', 'value': 'post-body'},
    {'attr': 'class', 'value': 'entry-content'},
    {'attr': 'itemprop', 'value': 'articleBody'},
    {'attr': 'id', 'value': 'mw-content-text'}, # wiki sites
    {'tag': 'article'},
    {'attr': 'class', 'value': 'transcripts'}, #slideshare
    {'attr': 'class', 'value': 'content'},
]

KNOWN_HOST_CONTENT_TAGS = {
    'www.ebay.com': '.vi-price, noscript [itemprop="image"], #vi-desc-maincntr, #Results, [itemprop="articleBody"]',
    'deals.ebay.com': { 'reference': 'www.ebay.com' },
    'www.ebay.co.uk': { 'reference': 'www.ebay.com' },
    'www.goal.com': '[itemprop="articleBody"]',
    'hk.apple.nextmedia.com': '.ArticleContent',
    'www.linkedin.com': '.discussion-content, .description-module, .company-module',
    'twitpic.com': '#media-main',
    'www.twitpic.com': { 'reference': 'twitpic.com' },
    '500px.com': '.the_photo, .description',
    'designspiration.net': '#ImageModule .saveImage, #ImageModule .saveDescription, #ImageModule .accreditationLink',
    'slickdeals.net': '#dealTextContainer, #dealTextContainer, .textDescription, .editorsNotes, [itemprop="description"]',
    'ask.fm': '#profile-picture, .questionBox',
    'stackoverflow.com': '#question .post-text, #question .owner .user-info, .accepted-answer .post-text, .accepted-answer .user-info',
    'serverfault.com': { 'reference': 'stackoverflow.com' },
    'superuser.com': { 'reference': 'stackoverflow.com' },
    'askubuntu.com': { 'reference': 'stackoverflow.com' },
    'stackapps.com': { 'reference': 'stackoverflow.com' },
    'mathoverflow.net': { 'reference': 'stackoverflow.com' },
    'regexs_references': {
        'stackoverflow.com$|stackexchange.com$': { 'reference': 'stackoverflow.com' },
    },
    'github.com': '[itemprop="mainContentOfPage"], [itemtype="http://schema.org/Person"], .org-header-wrapper, .blog-post-body',
    'timesofindia.indiatimes.com': '.storydiv .Normal',
    'www.lomography.com': '.content article, .content .detail, .content .meta',
    'www.businessinsider.com': '.post-content',
    'www.etsy.com': '#listing-page-cart, #image-carousel img, #description, .avatar, #bio, #shop-announcement-overlay .overlay-body, #shop_banner, .primary.view .listing-card',
    'www.mashreghnews.ir': '.news_body',
    'itunes.apple.com': '.intro, [itemprop="description"], .product-review',
    'www.yahoo.com': '.content',
    'lesson-school.com': '.post-single-text',
    'www.entrepreneur.com': '.article-body',
    'www.lapatilla.com': '.entry-content',
    'medium.com': '.postField',
    'reporte.us': '.noticia',
    'www.reporte.us': { 'reference': 'reporte.us' },
    'www.npr.org': '.storylocation',
    'blogs.wsj.com': '.post-content, #dMainContent',
    'www.huffingtonpost.co.uk': '#mainentrycontent',
    'www.huffingtonpost.com': { 'reference': 'www.huffingtonpost.co.uk' },
    'route.newsactus.com': '.article .left-part p',
}



class ContentExtractor(object):

    def __init__(self, config, article):
        # config
        self.config = config

        # parser
        self.parser = self.config.get_parser()

        # article
        self.article = article

        # language
        self.language = config.target_language

        # stopwords class
        self.stopwords_class = config.stopwords_class

    def clean_title(self, title):
        """Clean title with the use of og:site_name
        in this case try to get ride of site name
        and use TITLE_SPLITTERS to reformat title
        """
        if len(title) == 0:
            return title
        # check if we have the site name in opengraph data
        if "site_name" in self.article.opengraph.keys():
            site_name = self.article.opengraph['site_name']
            # remove the site name from title
            title = title.replace(site_name, '').strip()

        # try to remove the domain from url
        if self.article.domain:
            pattern = re.compile(self.article.domain, re.IGNORECASE)
            title = pattern.sub("", title).strip()

        # split the title in words
        # TechCrunch | my wonderfull article
        # my wonderfull article | TechCrunch
        title_words = title.split()

        if len(title_words) == 0:
            return title

        # check if first letter is in TITLE_SPLITTERS
        # if so remove it
        if title_words[0] in TITLE_SPLITTERS:
            title_words.pop(0)

        # check if last letter is in TITLE_SPLITTERS
        # if so remove it
        if title_words[-1] in TITLE_SPLITTERS:
            title_words.pop(-1)

        # rebuild the title
        title = u" ".join(title_words).strip()

        return title

    def get_title(self):
        """\
        Fetch the article title and analyze it
        """

        title = ''

        # rely on opengraph in case we have the data
        if "title" in self.article.opengraph.keys():
            title = self.article.opengraph['title']
            return self.clean_title(title)

        # try to fetch the meta headline
        meta_headline = self.parser.getElementsByTag(
                            self.article.doc,
                            tag="meta",
                            attr="name",
                            value="headline")
        if meta_headline is not None and len(meta_headline) > 0:
            title = self.parser.getAttribute(meta_headline[0], 'content')
            return self.clean_title(title)

        # otherwise use the title meta
        title_element = self.parser.getElementsByTag(self.article.doc, tag='title')
        if title_element is not None and len(title_element) > 0:
            title = self.parser.getText(title_element[0])
            return self.clean_title(title)

        return title

    def split_title(self, title, splitter):
        """\
        Split the title to best part possible
        """
        large_text_length = 0
        large_text_index = 0
        title_pieces = splitter.split(title)

        # find the largest title piece
        for i in range(len(title_pieces)):
            current = title_pieces[i]
            if len(current) > large_text_length:
                large_text_length = len(current)
                large_text_index = i

        # replace content
        title = title_pieces[large_text_index]
        return TITLE_REPLACEMENTS.replaceAll(title).strip()

    def get_publish_date(self):
        return self.get_from_known_meta_tags(KNOWN_PUBLISH_DATE_META_TAGS)


    def get_opengraph(self):
        opengraph_dict = {}
        node = self.article.doc
        metas = self.parser.getElementsByTag(node, 'meta')
        for meta in metas:
            attr = self.parser.getAttribute(meta, 'property')
            if attr is not None and attr.startswith("og:"):
                value = self.parser.getAttribute(meta, 'content')
                opengraph_dict.update({attr.split(":")[1]: value})
        return opengraph_dict

    def get_from_known_meta_tags(self, known_meta_tags):
        for known_meta_tag in known_meta_tags:
            meta_tags = self.parser.getElementsByTag(self.article.doc,
                                                tag='meta',
                                                attr=known_meta_tag['attribute'],
                                                value=known_meta_tag['value'])
            if meta_tags:
                return self.parser.getAttribute(meta_tags[0], attr='content')

    def get_favicon(self):
        """\
        Extract the favicon from a website
        http://en.wikipedia.org/wiki/Favicon
        <link rel="shortcut icon" type="image/png" href="favicon.png" />
        <link rel="icon" type="image/png" href="favicon.png" />
        """
        kwargs = {'tag': 'link', 'attr': 'rel', 'value': 'icon'}
        meta = self.parser.getElementsByTag(self.article.doc, **kwargs)
        if meta:
            favicon = self.parser.getAttribute(meta[0], 'href')
            return favicon
        return ''

    def get_meta_lang(self):
        """\
        Extract content language from meta
        """
        # we have a lang attribute in html
        attr = self.parser.getAttribute(self.article.doc, attr='lang')
        if attr is None:
            # look up for a Content-Language in meta
            items = [
                {'tag': 'meta', 'attr': 'http-equiv', 'value': 'content-language'},
                {'tag': 'meta', 'attr': 'name', 'value': 'lang'}
            ]
            for item in items:
                meta = self.parser.getElementsByTag(self.article.doc, **item)
                if meta:
                    attr = self.parser.getAttribute(meta[0], attr='content')
                    break

        if attr:
            value = attr[:2]
            if re.search(RE_LANG, value):
                return value.lower()

        return None

    def get_meta_content(self, doc, metaName):
        """\
        Extract a given meta content form document
        """
        meta = self.parser.css_select(doc, metaName)
        content = None

        if meta is not None and len(meta) > 0:
            content = self.parser.getAttribute(meta[0], 'content')

        if content:
            return content.strip()

        return ''

    def get_meta_description(self):
        return self.get_from_known_meta_tags(KNOWN_DESCRIPTION_META_TAGS)

    def get_meta_keywords(self):
        """\
        if the article has meta keywords set in the source, use that
        """
        return self.get_meta_content(self.article.doc, "meta[name=keywords]")

    def get_canonical_link(self):
        """\
        if the article has meta canonical link set in the url
        """
        if self.article.final_url:
            kwargs = {'tag': 'link', 'attr': 'rel', 'value': 'canonical'}
            meta = self.parser.getElementsByTag(self.article.doc, **kwargs)
            if meta is not None and len(meta) > 0:
                href = self.parser.getAttribute(meta[0], 'href')
                if href:
                    href = href.strip()
                    o = urlparse(href)
                    if not o.hostname:
                        z = urlparse(self.article.final_url)
                        domain = '%s://%s' % (z.scheme, z.hostname)
                        href = urljoin(domain, href)
                    return href
        return self.article.final_url

    def get_domain(self):
        if self.article.final_url:
            o = urlparse(self.article.final_url)
            return o.hostname
        return None

    def extract_tags(self):
        node = self.article.doc

        # node doesn't have chidren
        if len(list(node)) == 0:
            return NO_STRINGS

        elements = self.parser.css_select(node, A_REL_TAG_SELECTOR)
        if not elements:
            elements = self.parser.css_select(node, A_HREF_TAG_SELECTOR)
            if not elements:
                return NO_STRINGS

        tags = []
        for el in elements:
            tag = self.parser.getText(el)
            if tag:
                tags.append(tag)

        return set(tags)

    def calculate_best_node(self):
        top_host_node_from_known_tags = self.get_top_host_node_from_known_tags()
        if top_host_node_from_known_tags is not None:
            return top_host_node_from_known_tags

        top_node_from_known_tags = self.get_top_node_from_known_tags()
        if top_node_from_known_tags is not None:
            return top_node_from_known_tags

        doc = self.article.doc
        top_node = None
        nodes_to_check = self.nodes_to_check(doc)

        starting_boost = float(1.0)
        cnt = 0
        i = 0
        parent_nodes = []
        nodes_with_text = []

        for node in nodes_to_check:
            text_node = self.parser.getText(node)
            word_stats = self.stopwords_class(language=self.language).get_stopword_count(text_node)
            high_link_density = self.is_highlink_density(node)
            if word_stats.get_stopword_count() > 2 and not high_link_density:
                nodes_with_text.append(node)

        nodes_number = len(nodes_with_text)
        negative_scoring = 0
        bottom_negativescore_nodes = float(nodes_number) * 0.25

        for node in nodes_with_text:
            boost_score = float(0)
            # boost
            if(self.is_boostable(node)):
                if cnt >= 0:
                    boost_score = float((1.0 / starting_boost) * 50)
                    starting_boost += 1
            # nodes_number
            if nodes_number > 15:
                if (nodes_number - i) <= bottom_negativescore_nodes:
                    booster = float(bottom_negativescore_nodes - (nodes_number - i))
                    boost_score = float(-pow(booster, float(2)))
                    negscore = abs(boost_score) + negative_scoring
                    if negscore > 40:
                        boost_score = float(5)

            text_node = self.parser.getText(node)
            word_stats = self.stopwords_class(language=self.language).get_stopword_count(text_node)
            upscore = int(word_stats.get_stopword_count() + boost_score)

            # parent node
            parent_node = self.parser.getParent(node)
            self.update_score(parent_node, upscore)
            self.update_node_count(parent_node, 1)

            if parent_node not in parent_nodes:
                parent_nodes.append(parent_node)

            # parentparent node
            parent_parent_node = self.parser.getParent(parent_node)
            if parent_parent_node is not None:
                self.update_node_count(parent_parent_node, 1)
                self.update_score(parent_parent_node, upscore / 2)
                if parent_parent_node not in parent_nodes:
                    parent_nodes.append(parent_parent_node)
            cnt += 1
            i += 1

        top_node_score = 0
        for e in parent_nodes:
            score = self.get_score(e)

            if score > top_node_score:
                top_node = e
                top_node_score = score

            if top_node is None:
                top_node = e

        return top_node

    def set_known_host_content_tags(self):
        self.known_host_content_tags = HostUtils.host_selectors(KNOWN_HOST_CONTENT_TAGS,
                                                                self.article.domain)

    def get_top_host_node_from_known_tags(self):
        self.set_known_host_content_tags()
        if self.known_host_content_tags:
            content_tags = self.parser.css_select(self.article.doc, self.known_host_content_tags)

            return self.parser.combine_nodes(content_tags)

    def get_top_node_from_known_tags(self):
        for item in KNOWN_CONTENT_TAGS:
            content_tags = self.parser.getElementsByTag(self.article.doc,
                                                        **item)
            content_tags = self.parser.combine_nodes(content_tags)
            if content_tags:
                return content_tags

    def is_boostable(self, node):
        """\
        alot of times the first paragraph might be the caption under an image
        so we'll want to make sure if we're going to boost a parent node that
        it should be connected to other paragraphs,
        at least for the first n paragraphs so we'll want to make sure that
        the next sibling is a paragraph and has at
        least some substatial weight to it
        """
        para = "p"
        steps_away = 0
        minimum_stopword_count = 5
        max_stepsaway_from_node = 3

        nodes = self.walk_siblings(node)
        for current_node in nodes:
            # p
            current_node_tag = self.parser.getTag(current_node)
            if current_node_tag == para:
                if steps_away >= max_stepsaway_from_node:
                    return False
                paraText = self.parser.getText(current_node)
                word_stats = self.stopwords_class(language=self.language).get_stopword_count(paraText)
                if word_stats.get_stopword_count() > minimum_stopword_count:
                    return True
                steps_away += 1
        return False

    def walk_siblings(self, node):
        current_sibling = self.parser.previousSibling(node)
        b = []
        while current_sibling is not None:
            b.append(current_sibling)
            previousSibling = self.parser.previousSibling(current_sibling)
            current_sibling = None if previousSibling is None else previousSibling
        return b

    def add_siblings(self, top_node):
        baselinescore_siblings_para = self.get_siblings_score(top_node)
        results = self.walk_siblings(top_node)
        for current_node in results:
            ps = self.get_siblings_content(current_node, baselinescore_siblings_para)
            for p in ps:
                top_node.insert(0, p)
        return top_node

    def replace_attributes(self, top_node, tag_name, old_attribute_name, new_attribute_name):
        css_path = tag_name + '[' + new_attribute_name + ']' # e.g. 'img[data-src]'
        for tag in self.parser.css_select(top_node, css_path):
            new_attribute_content = self.parser.getAttribute(tag, attr = new_attribute_name)
            self.parser.setAttribute(tag, old_attribute_name, new_attribute_content)

    def build_tag_paths(self, top_node, tag_name, attribute):
        for tag in self.parser.getElementsByTag(top_node, tag=tag_name):
            path = self.parser.getAttribute(tag, attr=attribute)
            if path is None:
                continue
            parsed_url = urlparse(path)
            if not parsed_url.hostname:
                url = urljoin(self.article.final_url, path)
                self.parser.setAttribute(tag, attribute, url)

    def get_siblings_content(self, current_sibling, baselinescore_siblings_para):
        """\
        adds any siblings that may have a decent score to this node
        """
        if current_sibling.tag == 'p' and len(self.parser.getText(current_sibling)) > 0:
            e0 = current_sibling
            if e0.tail:
                e0 = deepcopy(e0)
                e0.tail = ''
            return [e0]
        else:
            potential_paragraphs = self.parser.getElementsByTag(current_sibling, tag='p')
            if potential_paragraphs is None:
                return None
            else:
                ps = []
                for first_paragraph in potential_paragraphs:
                    text = self.parser.getText(first_paragraph)
                    if len(text) > 0:
                        word_stats = self.stopwords_class(language=self.language).get_stopword_count(text)
                        paragraph_score = word_stats.get_stopword_count()
                        sibling_baseline_score = float(.30)
                        high_link_density = self.is_highlink_density(first_paragraph)
                        score = float(baselinescore_siblings_para * sibling_baseline_score)
                        if score < paragraph_score and not high_link_density:
                            p = self.parser.createElement(tag='p', text=text, tail=None)
                            ps.append(p)
                return ps

    def get_siblings_score(self, top_node):
        """\
        we could have long articles that have tons of paragraphs
        so if we tried to calculate the base score against
        the total text score of those paragraphs it would be unfair.
        So we need to normalize the score based on the average scoring
        of the paragraphs within the top node.
        For example if our total score of 10 paragraphs was 1000
        but each had an average value of 100 then 100 should be our base.
        """
        base = 100000
        paragraphs_number = 0
        paragraphs_score = 0
        nodes_to_check = self.parser.getElementsByTag(top_node, tag='p')

        for node in nodes_to_check:
            text_node = self.parser.getText(node)
            word_stats = self.stopwords_class(language=self.language).get_stopword_count(text_node)
            high_link_density = self.is_highlink_density(node)
            if word_stats.get_stopword_count() > 2 and not high_link_density:
                paragraphs_number += 1
                paragraphs_score += word_stats.get_stopword_count()

        if paragraphs_number > 0:
            base = paragraphs_score / paragraphs_number

        return base

    def update_score(self, node, addToScore):
        """\
        adds a score to the gravityScore Attribute we put on divs
        we'll get the current score then add the score
        we're passing in to the current
        """
        current_score = 0
        score_string = self.parser.getAttribute(node, 'gravityScore')
        if score_string:
            current_score = int(score_string)

        new_score = current_score + addToScore
        self.parser.setAttribute(node, "gravityScore", str(new_score))

    def update_node_count(self, node, add_to_count):
        """\
        stores how many decent nodes are under a parent node
        """
        current_score = 0
        count_string = self.parser.getAttribute(node, 'gravityNodes')
        if count_string:
            current_score = int(count_string)

        new_score = current_score + add_to_count
        self.parser.setAttribute(node, "gravityNodes", str(new_score))

    def is_highlink_density(self, e):
        """\
        checks the density of links within a node,
        is there not much text and most of it contains linky shit?
        if so it's no good
        """
        links = self.parser.getElementsByTag(e, tag='a')
        if links is None or len(links) == 0:
            return False

        text = self.parser.getText(e)
        words = text.split(' ')
        words_number = float(len(words))
        sb = []
        for link in links:
            sb.append(self.parser.getText(link))

        linkText = ''.join(sb)
        linkWords = linkText.split(' ')
        numberOfLinkWords = float(len(linkWords))
        numberOfLinks = float(len(links))
        linkDivisor = float(numberOfLinkWords / words_number)
        score = float(linkDivisor * numberOfLinks)
        if score >= 1.0:
            return True
        return False
        # return True if score > 1.0 else False

    def get_score(self, node):
        """\
        returns the gravityScore as an integer from this node
        """
        return self.get_node_gravity_score(node) or 0

    def get_node_gravity_score(self, node):
        grvScoreString = self.parser.getAttribute(node, 'gravityScore')
        if not grvScoreString:
            return None
        return int(grvScoreString)

    def nodes_to_check(self, doc):
        """\
        returns a list of nodes we want to search
        on like paragraphs and tables
        """
        nodes_to_check = []
        for tag in ['p', 'pre', 'td', 'blockquote']:
            items = self.parser.getElementsByTag(doc, tag=tag)
            nodes_to_check += items
        return nodes_to_check

    def is_table_and_no_para_exist(self, e):
        subParagraphs = self.parser.getElementsByTag(e, tag='p')
        for p in subParagraphs:
            txt = self.parser.getText(p)
            if len(txt) < 25:
                self.parser.remove(p)

        subParagraphs2 = self.parser.getElementsByTag(e, tag='p')
        if len(subParagraphs2) == 0 and e.tag != "td":
            return True
        return False

    def have_images(self, element):
        images = self.parser.getElementsByTag(element, tag='img')
        if len(images) > 0:
            return True
        return False

    def is_nodescore_threshold_met(self, node, e):
        top_node_score = self.get_score(node)
        current_nodeScore = self.get_score(e)
        thresholdScore = float(top_node_score * .08)

        if (current_nodeScore < thresholdScore) and \
            e.tag != 'td':
            return False
        return True

    def post_cleanup(self):
        """\
        remove any divs that looks like non-content,
        clusters of links, or paras with no gusto
        """
        targetNode = self.article.top_node
        node = self.add_siblings(targetNode)

        # fixing nytimes images
        self.replace_attributes(node,
                                tag_name = 'img',
                                old_attribute_name = 'src',
                                new_attribute_name = 'data-src')

        # fixing ebay images
        self.replace_attributes(node,
                                tag_name = 'img',
                                old_attribute_name = 'src',
                                new_attribute_name = 'imgurl')

        self.build_tag_paths(node, 'img', 'src')
        self.build_tag_paths(node, 'a', 'href')
        allowed_tags = ['p', 'img', 'ul', 'ol', 'h2', 'h3', 'h4', 'h5', 'h6',
                        'strong', 'em', 'blockquote']

        if self.known_host_content_tags:
            return node

        for e in self.parser.getChildren(node):
            e_tag = self.parser.getTag(e)
            if e_tag not in allowed_tags:
                if (self.is_highlink_density(e) \
                    or self.is_table_and_no_para_exist(e) \
                    or not self.is_nodescore_threshold_met(node, e)) \
                    and not self.have_images(e):
                    self.parser.remove(e)
        return node


class StandardContentExtractor(ContentExtractor):
    pass
