# cspell: ignore Xcolored

"""
NAME: markdown_ext.py

A module that implements a few custom markdown extensions. The extensions are
put into three parts: The first is a pattern class, "{extension}Pattern", which
is used internally. The second is a markdown extension class,
"{extension}Extension", which can be instantiated and passed to
markdown.markdown()'s extensions key word argument. The third is an instance of
the extension class, which is placed into the extensions list.

Properties:

* Highlight
    > Turns the syntax ==highlighted text== into 'highlighted text' highlighted
    > yellow. This is done by creating a span with the class 'highlight'.
* Strikethrough
    > Turns the syntax ~~strikethrough text~~ into 'strikethrough text' with a
    line through it. This is done by creating a del tag around the text.
* ColorSpan
    > Turns the syntax %Xcolored text%Y% into the text 'colored text' with some
    > colors added. X and Y are the color attributes to apply to the text. The
    > first one, X, is required, while Y is optional. Because of this, the
    > syntax %Xcolored%% is also valid.
    >
    > Color attributes:
    > - Hex digits 0-7: 3-bit foreground colors in the order black, red, green,
    >   yellow, blue, magenta, cyan, white.
    > - Hex digits 8-F: 3-bit background colors in the same order as the
    >   foreground colors.

The list 'extensions' is the best thing to import from this module, because it's
got everything added. A simple 'from markdown_ext import extensions as mde'
should be enough!
"""

# pylint: disable=wrong-import-order

# cspell: ignore inlinepatterns
import xml.etree.ElementTree as etree
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

# Logging to console
import logging
from logging import log, INFO, WARN, ERROR, CRITICAL, DEBUG # pylint: disable=unused-import

# cspell: ignore: levelname
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HighlightPattern(Pattern):
    """Return a span element representing the highlighted text."""
    def handleMatch(self, m):
        node = etree.Element('span')
        node.set('class', 'highlight')
        node.text = m.group(2)
        return node

class HighlightExtension(Extension):
    """Add support for ==highlighted text==."""
    def extendMarkdown(self, md):
        highlight_pattern = r'==(.*?)=='
        highlight_pattern = HighlightPattern(highlight_pattern, md)
        md.inlinePatterns.register(highlight_pattern, 'highlight', 175)

class StrikethroughPattern(Pattern):
    """Return a del element representing the deleted text."""
    def handleMatch(self, m):
        node = etree.Element('del')
        node.text = m.group(2)
        return node

class StrikethroughExtension(Extension):
    """Add support for ~~deleted text~~."""
    def extendMarkdown(self, md):
        strikethrough_pattern = r'~~(.*?)~~'
        strikethrough_pattern = StrikethroughPattern(strikethrough_pattern, md)
        md.inlinePatterns.register(strikethrough_pattern, 'strikethrough', 175)

class ColorSpanExtension(Extension):
    """
    Markdown extension to convert sequences like %S...%% to span with class cS,
    where S is a number 0-7.
    """
    def extendMarkdown(self, md):
        # cspell: ignore colorspan
        md.inlinePatterns.register(
            ColorSpanPattern(r'%([0-9a-fA-F])(.*?)(%([0-9a-fA-F]?)%)', md),
            'colorspan', 175
            )

class ColorSpanPattern(Pattern):
    """Return a span element representing the colored text."""
    def handleMatch(self, m):
        color1 = int(m.group(2),base=16)
        color2 = (-1
                if m.group(5) == '' else
                int(m.group(5),base=16))
        content = m.group(3)
        log(DEBUG, f"Rendered color block {repr((color1,color2))}")
        el = etree.Element('span')
        el.text = content
        # Set the class attribute to the color class
        # c0-c7 for foreground colors (indicated by 0-7)
        # b0-b7 for background colors (indicated by 8-F)
        # Subtracting 8 yields the background color
        # the second color is only added if needed
        el.set('class',
            (f'c{color1}'
                if color1 < 8 else
            f'b{color1-8}') +
            (' '+(
                f'c{color2}'
                if color2 < 8 else
                f'b{color2-8}')
            ) if color2 >= 0 else ''
            )
        return el

extensions = [
    HighlightExtension(),
    StrikethroughExtension(),
    ColorSpanExtension()
]
