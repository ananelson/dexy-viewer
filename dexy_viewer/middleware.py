import web
import os

class CustomStaticApp(web.httpserver.StaticApp):
    def translate_path(self, path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), path.lstrip("/"))

import posixpath
import urllib
class StaticMiddleware:
    """WSGI middleware for serving static files."""
    def __init__(self, app, prefix='/static/'):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        path = self.normpath(path)

        if path.startswith(self.prefix):
            return CustomStaticApp(environ, start_response)
        else:
            return self.app(environ, start_response)

    def normpath(self, path):
        path2 = posixpath.normpath(urllib.unquote(path))
        if path.endswith("/"):
            path2 += "/"
        return path2
