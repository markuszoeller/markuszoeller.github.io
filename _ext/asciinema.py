import os

from docutils import nodes
from docutils.parsers import rst as RST
from docutils.parsers.rst import Directive

from sphinx.util.fileutil import copy_asset


COLS_DEFAULT = 120
ROWS_DEFAULT = 30
POSTER_DEFAULT = "npt:0:00"  # "data:text/plain,Poster text"


class AsciinemaPlayerNode(nodes.General, nodes.Element):
    pass


class Asciinema(Directive):
    """Create a node for the asciinema player

    Example rst:

    .. asciinema:: echo.json

    Resulting doctree node:
        <asciinema-player src="/_asciinema/echo.json"
        cols="120"
        rows="30"
        poster="npt:0:00">
        </asciinema-player>
    """

    has_content = False
    required_arguments = 1
    option_spec = {
        "cols": RST.directives.positive_int,
        "rows": RST.directives.positive_int,
        "poster": RST.directives.unchanged,
    }
    # TODO: with version or migrate old casts? If migrate, how?

    def run(self):
        player_node = AsciinemaPlayerNode(
            src=self.arguments[0],
            cols=self.options.get("cols", COLS_DEFAULT),
            rows=self.options.get("rows", ROWS_DEFAULT),
            poster=self.options.get("poster", POSTER_DEFAULT)
        )
        return [player_node]


def visit_player_node(self, node):
    src = node.get("src")
    cols = node.get("cols")
    rows = node.get("rows")
    poster = node.get("poster")
    html = f'<asciinema-player src="/_asciinema/{src}" ' \
           f'cols="{cols}" ' \
           f'rows="{rows}" ' \
           f'poster="{poster}">' \
           f'</asciinema-player>'
    self.body.append(html)


def depart_player_node(self, node):
    pass


def page_handler(app, pagename, templatename, context, doctree):
    if not doctree:
        return
    # docutils docs: https://tristanlatr.github.io/apidocs/docutils/docutils.nodes.document.html
    asciinema_nodes = doctree.traverse(condition=AsciinemaPlayerNode)
    for node in asciinema_nodes:
        # `node.source` example: `/opt/shared/posts/2022/01/16/zsh-command-hooks/index.rst`
        asciicast_file = os.path.join(os.path.split(node.source)[0], node.attributes["src"])
        print(f"copying asciicast: {asciicast_file}")
        copy_asset(asciicast_file, os.path.join(app.outdir, '_asciinema'))


def setup(app):
    app.add_node(AsciinemaPlayerNode, html=(visit_player_node, depart_player_node))
    app.add_directive("asciinema", Asciinema)
    app.connect("html-page-context", page_handler)

    # TODO: for later to copy css and js files:
    #  https://github.com/sphinx-doc/sphinx/issues/1379#issuecomment-809006086

    # https://www.sphinx-doc.org/en/master/extdev/index.html#extension-metadata
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
