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
* SocialLink
    > Converts the syntax platform@username into a link to the user on that 
    > platform. If the platform needs an additional url, (for example, email
    > has an additional url), you add that after a second @ sign.
    > For example, email@name@example.com will become a mailto link to
    > name@example.com. Likewise, twitter@user will link to @user's twitter
    > page.
    > Social platforms are configured in the SOCIAL_LINKS dictionary. Please
    > edit it to your liking.
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

SOCIAL_LINKS = {
    # Format:
    # 'platform': {
    #     'url': 'link to username on the platform',
    #     'icon': 'nerd font unicode char', # nerd-font-icon-title
    #     'display': 'text to display on the link'
    # }
    # OR
    # 'platform': 'alias'
    #
    # the alias will refer to another platform.
    # this is useful for twitter because some people call it X.
    'github': {
        'url': 'https://github.com/{username}',
        'icon': '\uf09b', # nf-fa-github
        'display': '@{username}'
    },
    'email': {
        'url': 'mailto:{username}@{mailbox}',
        'icon': '\uf0e0', # nf-fa-envelope
        'display': '{username}@{mailbox}'
    },
    'tumblr': {
        'url': 'https://tumblr.com/{username}',
        'icon': '\uf173', # nf-fa-tumblr
        'display': '@{username}'
    },
    'youtube': {
        'url': 'https://youtube.com/@{username}',
        'icon': '\uf16a', # nf-fa-youtube
        'display': '{username}'
    },
    'matrix': {
        'url': 'https://matrix.to/#/@{username}:{mailbox}',
        'icon': '\uf27a', # nf-fa-message
        'display': '@{username}:{mailbox}'
    },
}

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
                f'b{color2-8}') if color2 >= 0 else ''
            ))
        return el

class SocialLinkExtension(Extension):
    """
    Markdown extension where platform@username becomes a link saying platform@username
    """
    SOCIAL_REGEX = (
        r'(?P<platform>[a-zA-Z0-9]+)'+
        r'@(?P<username>[a-zA-Z0-9_.\-+]+)'+
        r'(@(?P<mailbox>[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+))?'+
        r'(?=[,.!? ]|$)'
        )
    def extendMarkdown(self, md):
        """
        Register the pattern with the markdown instance.
        """
        social_pattern = SocialLinkPattern(self.SOCIAL_REGEX, md)
        md.inlinePatterns.register(social_pattern, 'social', 160)

class SocialLinkPattern(Pattern):
    """ Return a link element representing the social link. """
    def handleMatch(self, m):
        platform = m.group('platform')
        username = m.group('username')
        mailbox = m.group('mailbox')
        while True:
            # Unalias platform.
            if platform not in SOCIAL_LINKS:
                log(WARN, f"Unknown platform {platform} in {m.group(0)}")
                return None
            if isinstance(SOCIAL_LINKS[platform], str):
                # alias
                platform = SOCIAL_LINKS[platform]
                continue
            break
        # link
        el = etree.Element('a')
        el.set('class', f'social-link {platform}-link')
        url = SOCIAL_LINKS[platform]['url']
        url = url.format(username=username, mailbox=mailbox)
        el.set('href', url)
        # text
        text = SOCIAL_LINKS[platform]['display']
        text = text.format(username=username, mailbox=mailbox)
        icon = SOCIAL_LINKS[platform]['icon']
        el.text = icon + text
        # Open in new tab
        el.set('target', '_blank')
        el.set('rel', 'noopener noreferrer')
        # hover text
        el.set('title', f"{text} via {platform}")
        return el

extensions = [
    HighlightExtension(),
    StrikethroughExtension(),
    ColorSpanExtension(),
    SocialLinkExtension()
]
