"""Module to deal with remote server communications."""
import urllib.request

from proxy_content_handler import ProxyContentHandler


class ProxyClient:
    """A client to obtain, process and return static content from https://habr.com."""

    REMOTE_SERVER = "https://habr.com"

    def proxy_GET(self, handler):
        """GET the remote host, try to plocess content as required, return result."""
        url = f"{self.REMOTE_SERVER}{handler.path}"
        print(f"{url}\n")
        downstream_response = urllib.request.urlopen(url)
        content = downstream_response.read()
        content_type = downstream_response.info().get_content_type()
        encoding = downstream_response.info().get_content_charset()

        handler.set_headers(
            content_type,
            downstream_response.getcode()
        )
        if content_type == "text/html":
            try:
                content = content.decode(encoding)
                content_handler = ProxyContentHandler()
                content = content_handler.handle_absolute_local_links(content, self.REMOTE_SERVER)
                content = content_handler.handle_textual_content(content)
            except Exception:
                print("\n[*] Couldn't decode (incorrect MIME type). \n")

        return content
