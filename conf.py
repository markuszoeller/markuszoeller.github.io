# -*- coding: utf-8 -*-

# Markus's Brain Swap Space build configuration file, created by
# `ablog start` on Mon Nov 16 22:06:46 2015.
#
# Note that not all possible configuration values are present in this file.
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys
import ablog
import sphinx_bootstrap_theme


# To include my own extensions in this repo:
sys.path.append(os.path.abspath("./_ext"))


# -- General ABlog Options ----------------------------------------------------

# A path relative to the configuration directory for blog archive pages.
blog_path = 'posts'

# The “title” for the blog, used in acthive pages.  Default is ``'Blog'``.
blog_title = u'Markus\'s Brain Swap Space'

# Base URL for the website, required for generating feeds.
# e.g. blog_baseurl = "http://example.com/"
blog_baseurl = "http://www.markusz.io/"

# GitHub username for deploying to GitHub pages
github_pages = "markuszoeller"

# Choose to archive only post titles. Archiving only titles can speed
# up project building.
#blog_archive_titles = False

# -- Blog Authors, Languages, and Locations -----------------------------------

# A dictionary of author names mapping to author full display names and
# links. Dictionary keys are what should be used in ``post`` directive
# to refer to the author.  Default is ``{}``.
blog_authors = {
    'mz': ('Markus Zoeller', None),
}


blog_default_author = "mz"

# A dictionary of language code names mapping to full display names and
# links of these languages. Similar to :confval:`blog_authors`, dictionary
# keys should be used in ``post`` directive to refer to the locations.
# Default is ``{}``.
blog_languages = {
   'en': ('English', None),
}


# A dictionary of location names mapping to full display names and
# links of these locations. Similar to :confval:`blog_authors`, dictionary
# keys should be used in ``post`` directive to refer to the locations.
# Default is ``{}``.
#blog_locations = {
#    'Earth': ('The Blue Planet', 'http://en.wikipedia.org/wiki/Earth),
#}


# -- Blog Post Related --------------------------------------------------------

# post_date_format = '%b %d, %Y'


# Number of paragraphs (default is ``1``) that will be displayed as an excerpt
# from the post. Setting this ``0`` will result in displaying no post excerpt
# in archive pages.  This option can be set on a per post basis using
#post_auto_excerpt = 1

# Index of the image that will be displayed in the excerpt of the post.
# Default is ``0``, meaning no image.  Setting this to ``1`` will include
# the first image, when available, to the excerpt.  This option can be set
# on a per post basis using :rst:dir:`post` directive option ``image``.
#post_auto_image = 0

# Number of seconds (default is ``5``) that a redirect page waits before
# refreshing the page to redirect to the post.
#post_redirect_refresh = 5

# When ``True``, post title and excerpt is always taken from the section that
# contains the :rst:dir:`post` directive, instead of the document. This is the
# behavior when :rst:dir:`post` is used multiple times in a document. Default
# is ``False``.
#post_always_section = False

# -- ABlog Sidebars -------------------------------------------------------

# There are seven sidebars you can include in your HTML output.
# postcard.html provides information regarding the current post.
# recentposts.html lists most recent five posts. Others provide
# a link to a archive pages generated for each tag, category, and year.
# In addition, there are authors.html, languages.html, and locations.html
# sidebars that link to author and location archive pages.
html_sidebars = {}

# -- Blog Feed Options --------------------------------------------------------

# Turn feeds by setting :confval:`blog_baseurl` configuration variable.
# Choose to create feeds per author, location, tag, category, and year,
# default is ``False``.
#blog_feed_archives = False

# Choose to display full text in blog feeds, default is ``False``.
#blog_feed_fulltext = False

# Blog feed subtitle, default is ``None``.
#blog_feed_subtitle = None

# Choose to feed only post titles, default is ``False``.
#blog_feed_titles = False

# Specify number of recent posts to include in feeds, default is ``None``
# for all posts.
#blog_feed_length = None

# -- Font-Awesome Options -----------------------------------------------------

# ABlog templates will use of Font Awesome icons if one of the following
# is ``True``

# Link to `Font Awesome`_ at `Bootstrap CDN`_ and use icons in sidebars
# and post footers.  Default: ``False``
# fontawesome_link_cdn = "http://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"

# Sphinx_ theme already links to `Font Awesome`_.  Default: ``False``
#fontawesome_included = False

# Alternatively, you can provide the path to `Font Awesome`_ :file:`.css`
# with the configuration option: fontawesome_css_file
# Path to `Font Awesome`_ :file:`.css` (default is ``None``) that will
# be linked to in HTML output by ABlog.
#fontawesome_css_file = None

# -- Disqus Integration -------------------------------------------------------

# You can enable Disqus_ by setting ``disqus_shortname`` variable.
# Disqus_ short name for the blog.
disqus_shortname = ""

# Choose to disqus pages that are not posts, default is ``False``.
disqus_pages = False

# Choose to disqus posts that are drafts (without a published date),
# default is ``False``.
#disqus_drafts = False

# -- Sphinx Options -----------------------------------------------------------

# If your project needs a minimal Sphinx version, state it here.
needs_sphinx = '1.2'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.extlinks',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'alabaster',
    'ablog',
    'sphinxcontrib.spelling',
    'sphinxcontrib.blockdiag',
    'asciinema'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates', ablog.get_html_templates_path()]

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'MZIO'
copyright = u'2015-2022, Markus Zoeller'
author = u'Markus Zoeller'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['README.rst', '.venv', '.asciinema', '**/example-app']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for Graphviz -------------------------------------------------
graphviz_output_format = 'svg'


# -- Options for sphinxcontrib-spelling -----------------------------------
spelling_lang = 'en_US'
spelling_word_list_filename = 'spelling_wordlist.txt'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'bootstrap'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    # https://github.com/ryan-roemer/sphinx-bootstrap-theme
    'navbar_links': [
        ("About", "about"),
        ("Categories", "posts/category"),
        ("Tags", "posts/tag"),
        ("Archive", "posts/archive"),
        ("<i class='fa fa-rss-square' aria-hidden='true'></i>", "/posts/atom.xml", True),
    ],
    'globaltoc_includehidden': "false",
    'navbar_sidebarrel': False,
    'navbar_pagenav': False,
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "Markus Zoeller Blog"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# This value determines the text for the permalink; it defaults to "¶".
# Set it to None or the empty string to disable permalinks.
html_add_permalinks = " "
# html_permalinks_icon = ""
# html_permalinks = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'MyBrainSwapSpacedoc'


def setup(app):
    app.add_stylesheet('css/custom.css')  # may also be an URL
    app.add_stylesheet('https://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css')
    app.add_stylesheet('css/asciinema-player.css')
    app.add_javascript('js/asciinema-player.js')
    # app.add_css_file('css/custom.css')  # may also be an URL
    # app.add_css_file('http://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css')  # may also be an URL
    # app.add_css_file('css/asciinema-player.css')
    # app.add_js_file('js/asciinema-player.js')