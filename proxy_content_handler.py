import re

from bs4 import BeautifulSoup, NavigableString


class ProxyContentHandler:
    """
    A class to process static content, as follows:

    (1) Handle links, including svg/use tags and JS base constants:
        make links relative.

    (2) Modify textual content :
        add a trade mark sign after each six character long word rendered by the browser,
        with the exception of these within the code tag.

    Implementation:
        - extract all strings contained within HTML tags, sans nested tags,
        from the HTML content string using regex
        (appears more effective that traversing the DOM as requires no drilling down)
        - send selection to parse for specified (6 char long) words and apply modifications
        - parse the resulting HTML string semantically
        and remove modifications wherever they disrupt behavior
        (non-textual tags containing text e.g. script) and where they make no sense (eg the code tag);
        appears more effective as these are few and guaranteed to have no child tags subject to treatment
    """

    # Note: the utf-8 is more consistently supported by the parser than HTML entities
    TM = "™"

    # Select any text between tag closing and opening borders containing no nested tags,
    # multiline, logically lazy
    renderable_text_re = re.compile(r"""
        (?miux)>[^<>]+<
        """, re.VERBOSE)

    # Select non-textual tags and the code tags
    # (as expected by the BeautifulSoup DOM selector)
    non_textual_tags_re = re.compile(r"""
        ^(script|style|svg|path|code)
        """, re.VERBOSE)

    # Select words exactly six characters long,
    # regardless of their position in text, case insensitive
    six_character_words_re = re.compile(r"""
        \b\w{6}\b
        """, re.VERBOSE)

    @staticmethod
    def handle_absolute_local_links(content, REMOTE_SERVER):
        """Make links relative."""
        return content.replace(REMOTE_SERVER, "")

    def handle_textual_content(self, content):
        """Modify text rendered by browser, as per spec."""

        # Treat the specified occurrences within renderable text
        content = self.renderable_text_re.sub(self._modify_renderable_text, content)

        # Undo treatment where not needed
        soup = BeautifulSoup(self._prep_for_the_soup(content), "html.parser")

        for tag in soup.find_all(self.non_textual_tags_re):
            if tag.string is not None:
                tag_string = self._strip_trademarks(str(tag.string))
                tag.string.replace_with(NavigableString(tag_string))

        return soup.encode()

    @staticmethod
    def _prep_for_the_soup(content):
        # Address the parser's inconsistencies in rendering the &plus; entity
        return content.replace("&plus;", "&#43;")

    def _modify_renderable_text(self, match):
        return self.six_character_words_re.sub(self._add_trademark_to_selected, match.group(0))

    def _add_trademark_to_selected(self, match):
        return match.group(0) + self.TM

    def _strip_trademarks(self, string):
        return string.replace(self.TM, "")
