"""A simple HTTP server proxying requests to https://habr.com and serving its modified content.
"""
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import re
from bs4 import BeautifulSoup, NavigableString

DEFAULT_PORT = 8080
DEFAULT_HOST = '127.0.0.1'

class ProxyHandler(BaseHTTPRequestHandler):
    """Build a minimal handler on top of BaseHTTPRequestHandler.
    """

    REMOTE_SERVER = "https://habr.com"

    def do_GET(self):
        """Override do_GET superclass method with the proxy client.
        """
        self.wfile.write(self._proxy_client())

    def _proxy_client(self):
        downstream_response = urllib.request.urlopen(
            f"{self.REMOTE_SERVER}{self.path}"
        )
        content = downstream_response.read()
        content_type = downstream_response \
            .info() \
            .get_content_type()
        self._set_headers(
            content_type,
            downstream_response.getcode()
        )
        if content_type == 'text/html':
            content = self._process_text_content(content)
        return content

    def _set_headers(self, content_type, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def _process_text_content(self, content):
        """Modify text rendered by browser as per spec
        """
        content = content.decode('utf-8')
        # Replace hard links with relative ones
        content = content.replace(self.REMOTE_SERVER, '')

        # helper functions
        def modify_renderable_text(match):
            """Match words six characters long, send to be modified with the trade mark.
            """
            return re.sub(r'\b\w{6}\b', add_trademark_to_selected, match.group(0))

        def add_trademark_to_selected(match):
            """Add trade mark after input.
            """
            return match.group(0) + '&trade;'

        def strip_trademarks(match):
            """Add trade mark after input.
            """
            print(match.group(0))
            return match.group(0).replace('&trade;', '')

        # MODIFY TEXT:
        # select any text between tag closing and opening borders containing no nested tags,
        # send selection to parse for specified (6 char long) words,
        # then add trademarks to matched words
        renderable_text_re = re.compile(r"""
            (?miux)>[^<>]+<
            """, re.VERBOSE)
        content = renderable_text_re.sub(modify_renderable_text, content)

        # Unfortunately, while this is fast and effective,
        # it catches some non-textual tags;
        # fix these
        non_renderable_text_re = re.compile(r"""
            (?miuxs)<(script|style|svg|path).*?>(.*?)</\1>
            """, re.VERBOSE)
        content = non_renderable_text_re.sub(strip_trademarks, content)

        return content.encode('utf-8')

def run(server_class=HTTPServer, handler_class=ProxyHandler, addr=DEFAULT_HOST, port=DEFAULT_PORT):
    """Run the server.
    """
    httpd = server_class((addr, port), handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


try:
    LISTENING_PORT = int(input("[*] Enter Listening Port Number: [8080]") or DEFAULT_PORT)
    run(addr=DEFAULT_HOST, port=LISTENING_PORT)
except KeyboardInterrupt:
    print("\n[*] Exiting ... Have a nice day! \n")
    sys.exit()
