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
from goose.images.image import Image
import re


class ImageExtractor(object):
    def __init__(self, config, article):
        self.article = article
        self.config = config
        self.parser = self.config.get_parser()

    def get_images(self, top_node):
        return self.get_opengraph_tags() + self.get_content_images(top_node)

    def get_opengraph_tags(self):
        node = self.article.raw_doc
        meta = self.parser.getElementsByTag(node, tag='meta', attr='property', value='og:image')
        images = []
        for item in meta:
            if self.parser.getAttribute(item, attr='property') == 'og:image':
                src = self.parser.getAttribute(item, attr='content')
                if src:
                    images.append(self.from_image_node_to_image(item, src))
        return images

    def get_content_images(self, top_node):
        images = []
        image_nodes = self.parser.getElementsByTag(top_node, tag='img')
        for image_node in image_nodes:
            image = self.from_image_node_to_image(image_node)
            images.append(image)

        return images

    def from_image_node_to_image(self, image_node, src=None):
        image = Image()
        if src:
            image.src = src
        else:
            image.src = self.parser.getAttribute(image_node, 'src')
        image.width = self.size_to_int(image_node, 'width')
        image.height = self.size_to_int(image_node, 'height')

        return image

    def size_to_int(self, image_node, attribute_name):
        size = self.parser.getAttribute(image_node, attribute_name)
        if size is None:
            return None
        digits_only = re.sub("\D", "", size)
        if len(digits_only) is 0:
            return None

        return int(digits_only)
