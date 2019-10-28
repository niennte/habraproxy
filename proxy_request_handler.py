from http.server import BaseHTTPRequestHandler

from proxy_client import ProxyClient


class ProxyRequestHandler(BaseHTTPRequestHandler):
    """A minimal handler on top of BaseHTTPRequestHandler."""

    def do_GET(self):
        """Intercept the GET request and delegate to the proxy client."""
        client = ProxyClient()
        self.wfile.write(client.proxy_GET(self))

    def set_headers(self, content_type, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

