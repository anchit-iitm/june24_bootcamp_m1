import http.server
import socketserver
import mimetypes
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # Use the default MIME type guessing, but add PDF support if necessary
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type is None:
            if path.endswith('.pdf'):
                return 'application/pdf'
        return mime_type
PORT = 8000
Handler = CustomHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print(f"Serving at port {PORT}")
httpd.serve_forever()
