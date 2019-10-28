"""A simple HTTP server proxying requests to https://habr.com and serving its modified content."""
import sys
from http.server import HTTPServer

from proxy_request_handler import ProxyRequestHandler

DEFAULT_PORT = 8080
DEFAULT_HOST = "127.0.0.1"


def run(server_class=HTTPServer,
        handler_class=ProxyRequestHandler,
        addr=DEFAULT_HOST,
        port=DEFAULT_PORT):
    """Run the server."""
    httpd = server_class((addr, port), handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


try:
    LISTENING_PORT = int(input("[*] Enter Listening Port Number: [8080]") or DEFAULT_PORT)
    run(addr=DEFAULT_HOST, port=LISTENING_PORT)
except KeyboardInterrupt:
    print("\n[*] Exiting ... Have a nice day! \n")
    sys.exit()
