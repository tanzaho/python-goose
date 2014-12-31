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
from base import TestExtractionBase
import re

from base import BaseMockTests, MockResponse

from goose.text import StopWordsChinese
from goose.text import StopWordsArabic
from goose.text import StopWordsKorean

class TestExtractions(TestExtractionBase):

    def test_allnewlyrics1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnn1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek3(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cbslocal(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_elmondo1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_elpais(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_liberation(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_lefigaro(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_techcrunch1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_foxNews(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_aolNews(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_huffingtonPost2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_testHuffingtonPost(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'meta_description', 'title', ]
        self.runArticleAssertions(article=article, fields=fields)

    def test_espn(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_engadget(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_msn1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    # #########################################
    # # FAIL CHECK
    # # UNICODE
    # def test_guardian1(self):
    #     article = self.getArticle()
    #     fields = ['cleaned_text']
    #     self.runArticleAssertions(article=article, fields=fields)
    def test_time(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'title']
        self.runArticleAssertions(article=article, fields=fields)

    def test_time2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnet(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_yahoo(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_politico(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessinsider1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessinsider2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessinsider3(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnbc1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_marketplace(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue24(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue25(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue28(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue32(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue4(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_gizmodo1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'meta_description', 'meta_keywords']
        self.runArticleAssertions(article=article, fields=fields)

    def test_mashable_issue_74(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_usatoday_issue_74(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_okaymarketing(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_bbc(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_huffingtonpost(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_theguardian(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_blockquotes(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_clean_bad_tags(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_embedded_media_items(self):
        article = self.getArticle()
        self.assert_content_html(article)


class TestKnownHosts(TestExtractionBase):
    def test_known_host_selectors(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_known_host_selectors_with_regexs_references(self):
        article = self.getArticle()
        self.assert_content_html(article)


class TestRelativePaths(TestExtractionBase):

    def test_relative_paths(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_tags_with_no_path(self):
        article = self.getArticle()
        self.assert_content_html(article)

class TestReplacingAttributes(TestExtractionBase):

    def test_replacing_attributes(self):
        article = self.getArticle()
        self.assert_content_html(article)


class TestMetaDescription(TestExtractionBase):

    def test_meta_description(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=['meta_description'])


class TestExtractWithUrl(TestExtractionBase):

    def test_get_canonical_url(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'canonical_link']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractChinese(TestExtractionBase):

    def getConfig(self):
        config = super(TestExtractChinese, self).getConfig()
        config.stopwords_class = StopWordsChinese
        return config

    def test_bbc_chinese(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractArabic(TestExtractionBase):

    def getConfig(self):
        config = super(TestExtractArabic, self).getConfig()
        config.stopwords_class = StopWordsArabic
        return config

    def test_cnn_arabic(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractKorean(TestExtractionBase):

    def getConfig(self):
        config = super(TestExtractKorean, self).getConfig()
        config.stopwords_class = StopWordsKorean
        return config

    def test_donga_korean(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'meta_description', 'meta_keywords']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractionsRaw(TestExtractions):

    def extract(self, instance):
        article = instance.extract(raw_html=self.getRawHtml())
        return article

    def test_bbc(self):
        return 'pending'
