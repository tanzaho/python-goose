Python-Goose - Article Extractor |Build Status|
===============================================

Intro
-----

Goose was originally an article extractor written in Java that has most
recently (aug2011) been converted to a `scala project <https://github.com/GravityLabs/goose>`_.

This is a complete rewrite in python. The aim of the software is to
take any news article or article-type web page and not only extract what
is the main body of the article but also all meta data and most probable
image candidate.

Goose will try to extract the following information:

-  Main text of an article
-  Main image of article
-  Any Youtube/Vimeo movies embedded in article
-  Meta Description
-  Meta tags

The python version was rewritten by:

-  Xavier Grangier

Licensing
---------

If you find Goose useful or have issues please drop me a line. I'd love
to hear how you're using it or what features should be improved

Goose is licensed by Gravity.com under the Apache 2.0 license, see the
LICENSE file for more details

Setup
-----

::

    git clone git@github.com:cronycle/python-goose.git
    cd python-goose
    virtualenv --no-site-packages venv
    # Add "export API_KEY='ZZZZ'" to "venv/bin/activate"
    source venv/bin/activate
    pip install -r requirements.txt
    python setup.py install

Start the development server
------------------------

::

    python api/application.py

Take it for a spin
------------------

::

    >>> from goose import Goose
    >>> url = 'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2'
    >>> g = Goose()
    >>> article = g.extract(url=url)
    >>> article.title
    u'Occupy London loses eviction fight'
    >>> article.meta_description
    "Occupy London protesters who have been camped outside the landmark St. Paul's Cathedral for the past four months lost their court bid to avoid eviction Wednesday in a decision made by London's Court of Appeal."
    >>> article.content_html
    >>> article.images[0].src
    http://i2.cdn.turner.com/cnn/dam/assets/111017024308-occupy-london-st-paul-s-cathedral-story-top.jpg

Configuration
-------------

There are two ways to pass configuration to goose. The first one is to
pass goose a Configuration() object. The second one is to pass a
configuration dict.

For instance, if you want to change the userAgent used by Goose just
pass :

::

    >>> g = Goose({'browser_user_agent': 'Mozilla'})

Switching parsers : Goose can now be use with lxml html parser or lxml
soup parser. By default the html parser is used. If you want to use the
soup parser pass it in the configuration dict :

::

    >>> g = Goose({'browser_user_agent': 'Mozilla', 'parser_class':'soup'})

Goose is now language aware
---------------------------

For example scrapping a Spanish content page with correct meta language
tags

::

    >>> from goose import Goose
    >>> url = 'http://sociedad.elpais.com/sociedad/2012/10/27/actualidad/1351332873_157836.html'
    >>> g = Goose()
    >>> article = g.extract(url=url)
    >>> article.title
    u'Las listas de espera se agravan'
    >>> article.content_html

Some pages don't have correct meta language tags, you can force it using
configuration :

::

    >>> from goose import Goose
    >>> url = 'http://www.elmundo.es/elmundo/2012/10/28/espana/1351388909.html'
    >>> g = Goose({'use_meta_language': False, 'target_language':'es'})
    >>> article = g.extract(url=url)
    >>> article.content_html

Passing {'use\_meta\_language': False, 'target\_language':'es'} will
force as configuration will force the spanish language


Video extraction
----------------

::

    >>> import goose
    >>> url = 'http://www.liberation.fr/politiques/2013/08/12/journee-de-jeux-pour-ayrault-dans-les-jardins-de-matignon_924350'
    >>> g = goose.Goose({'target_language':'fr'})
    >>> article = g.extract(url=url)
    >>> article.movies
    [<goose.videos.videos.Video object at 0x25f60d0>]
    >>> article.movies[0].src
    'http://sa.kewego.com/embed/vp/?language_code=fr&playerKey=1764a824c13c&configKey=dcc707ec373f&suffix=&sig=9bc77afb496s&autostart=false'
    >>> article.movies[0].embed_code
    '<iframe src="http://sa.kewego.com/embed/vp/?language_code=fr&amp;playerKey=1764a824c13c&amp;configKey=dcc707ec373f&amp;suffix=&amp;sig=9bc77afb496s&amp;autostart=false" frameborder="0" scrolling="no" width="476" height="357"/>'
    >>> article.movies[0].embed_type
    'iframe'
    >>> article.movies[0].width
    '476'
    >>> article.movies[0].height
    '357'


Goose in Chinese
----------------

Some users want to use Goose for Chinese content. Chinese word
segmentation is way more difficult to deal with than occidental
languages. Chinese needs a dedicated StopWord analyser that need to be
passed to the config object

::

    >>> from goose import Goose
    >>> from goose.text import StopWordsChinese
    >>> url  = 'http://www.bbc.co.uk/zhongwen/simp/chinese_news/2012/12/121210_hongkong_politics.shtml'
    >>> g = Goose({'stopwords_class': StopWordsChinese})
    >>> article = g.extract(url=url)
    >>> print article.content_html

Goose in Arabic
---------------

In order to use Goose in Arabic you have to use the StopWordsArabic
class.

::

    >>> from goose import Goose
    >>> from goose.text import StopWordsArabic
    >>> url = 'http://arabic.cnn.com/2013/middle_east/8/3/syria.clashes/index.html'
    >>> g = Goose({'stopwords_class': StopWordsArabic})
    >>> article = g.extract(url=url)
    >>> print article.content_html

Goose in Korean
----------------

In order to use Goose in Korean you have to use the StopWordsKorean
class.

::

    >>> from goose import Goose
    >>> from goose.text import StopWordsKorean
    >>> url='http://news.donga.com/3/all/20131023/58406128/1'
    >>> g = Goose({'stopwords_class':StopWordsKorean})
    >>> article = g.extract(url=url)
    >>> print article.content_html

Known issues
------------

- There are some issues with unicode URLs.
- Cookie handling : Some websites need cookie handling. At the moment the only work around is to use the raw_html extraction. For instance ;

    >>> import urllib2
    >>> import goose
    >>> url = "http://www.nytimes.com/2013/08/18/world/middleeast/pressure-by-us-failed-to-sway-egypts-leaders.html?hp"
    >>> opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    >>> response = opener.open(url)
    >>> raw_html = response.read()
    >>> g = goose.Goose()
    >>> a = g.extract(raw_html=raw_html)
    >>> a.content_html

TODO
----

-  Video html5 tag extraction


.. |Build Status| image:: https://travis-ci.org/grangier/python-goose.png?branch=develop   :target: https://travis-ci.org/grangier/python-goose
