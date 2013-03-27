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
import os
import glob
from copy import deepcopy
from goose.article import Article
from goose.utils import URLHelper
from goose.extractors import StandardContentExtractor
from goose.cleaners import StandardDocumentCleaner
from goose.outputformatters import StandardOutputFormatter
from goose.parsers import Parser
from goose.images.extractors import UpgradedImageIExtractor
from goose.network import HtmlFetcher


class CrawlCandidate(object):

    def __init__(self, config, url, raw_html):
        self.config = config
        self.url = url
        self.raw_html = raw_html


class Crawler(object):

    def __init__(self, config):
        self.config = config
        self.logPrefix = "crawler:"

    def crawl(self, crawl_candidate):
        article = Article()

        parse_candidate = URLHelper.getCleanedUrl(crawl_candidate.url)
        raw_html = self.get_html(crawl_candidate, parse_candidate)

        if raw_html is None:
            return article

        doc = self.get_document(parse_candidate.url, raw_html)

        extractor = self.get_extractor()
        document_cleaner = self.get_document_cleaner()
        output_formatter = self.get_output_formatter()

        # article
        article.final_url = parse_candidate.url
        article.link_hash = parse_candidate.link_hash
        article.raw_html = raw_html
        article.doc = doc
        article.raw_doc = deepcopy(doc)
        article.title = extractor.get_title(article)
        # TODO
        # article.publish_date = config.publishDateExtractor.extract(doc)
        # article.additional_data = config.get_additionaldata_extractor.extract(doc)
        article.meta_lang = extractor.get_meta_lang(article)
        article.meta_favicon = extractor.get_favicon(article)
        article.meta_description = extractor.get_meta_description(article)
        article.meta_keywords = extractor.get_meta_keywords(article)
        article.canonical_link = extractor.get_canonical_link(article)
        article.domain = extractor.get_domain(article.final_url)
        article.tags = extractor.extract_tags(article)
        # # before we do any calcs on the body itself let's clean up the document
        article.doc = document_cleaner.clean(article)

        # big stuff
        article.top_node = extractor.calculate_best_node(article)
        if article.top_node is not None:
            # TODO
            # movies and images
            # article.movies = extractor.extractVideos(article.top_node)
            if self.config.enable_image_fetching:
                image_extractor = self.get_image_extractor(article)
                article.top_image = image_extractor.getBestImage(article.raw_doc, article.top_node)

            article.top_node = extractor.post_cleanup(article.top_node)
            article.cleaned_text = output_formatter.getFormattedText(article)

        # cleanup tmp file
        self.relase_resources(article)

        return article

    def get_html(self, crawl_candidate, parsing_candidate):
        if crawl_candidate.raw_html:
            return crawl_candidate.raw_html
        else:
            # fetch HTML
            html = HtmlFetcher().get_html(self.config, parsing_candidate.url)
            return html

    def get_image_extractor(self, article):
        httpClient = None
        return UpgradedImageIExtractor(httpClient, article, self.config)

    def get_output_formatter(self):
        return StandardOutputFormatter(self.config)

    def get_document_cleaner(self):
        return StandardDocumentCleaner()

    def get_document(self, url, raw_html):
        doc = Parser.fromstring(raw_html)
        return doc

    def get_extractor(self):
        return StandardContentExtractor(self.config)

    def relase_resources(self, article):
		# FIXEME : use os.path.join
        path = '%s/%s_*' % (self.config.local_storage_path, article.link_hash)
        for fname in glob.glob(path):
            try:
                os.remove(fname)
            except OSError:
                # TODO better log handeling
                pass
