from docutils import nodes
from docutils.utils.math import unichar2tex, math2html

from pelican import signals
from pelican import readers


class PelicanHTMLTranslator(readers.PelicanHTMLTranslator):

    def visit_math(self, node, math_env=''):
        tag = ('div', 'span')[math_env == '']
        math_code = node.astext().translate(unichar2tex.uni2tex_table)
        start_tag = self.starttag(node, tag, suffix='\n', CLASS='formula', ALT=math_code)

        math2html.DocumentParameters.displaymode = (math_env != '')
        math_code = math2html.math2html(math_code)

        self.body.append(start_tag)
        self.body.append(math_code)
        if math_env:
            self.body.append('\n')
        self.body.append('</%s>\n' % tag)
        raise nodes.SkipNode

def patch_readers_module(_readers):
    readers.PelicanHTMLTranslator = PelicanHTMLTranslator

def register():
    signals.readers_init.connect(patch_readers_module)
