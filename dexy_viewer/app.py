import web
import os
import json
from dexy.commands.utils import init_wrapper
from operator import attrgetter
from dexy.batch import Batch

urls = (
        '/favicon.ico', 'favicon',
        '/doc/(.*)', 'document',
        '/raw/(.*)', 'raw',
        '/snip/(.*)/(.*)', 'snippet',
        '/(.*)/(.*)', 'grep',
        '/(.*)', 'grep'
        )

render = web.template.render(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'))

wrapper = init_wrapper({})

def wrap_content(content, ext):
    # Add other extensions here with special handling needs. Default is wrapped in <pre> tags.
    if ext == ".html":
        return content
    else:
        return "<pre>\n%s\n</pre>" % content

class favicon:
    def GET(self):
        return ''

class grep:
    def GET(self, expr, keyexpr=None):
        batch = Batch.load_most_recent(wrapper)

        if not expr:
            matches = sorted([data for data in batch], key=attrgetter('key'))[0:20]
        else:
            matches = sorted([data for data in batch if expr in data.key], key=attrgetter('key'))

        return render.grep(matches, expr, keyexpr)

class raw:
    def GET(self, storage_key):
        batch = Batch.load_most_recent(wrapper)
        data = batch.data_for_storage_key(storage_key)
        try:
            json.dumps(unicode(data))
            return unicode(data)
        except UnicodeDecodeError:
            return data.data()

# TODO fix raw/document output for sectioned/key-value data

class document:
    def GET(self, storage_key):
        batch = Batch.load_most_recent(wrapper)
        data = batch.data_for_storage_key(storage_key)

        if data.ext in (".png", ".jpg"): # Add any other image formats here.
            return """<img title="%s" src="/raw/%s" />""" % (data.key, storage_key)
        else:
            try:
                uc = unicode(data)
                json.dumps(uc)
                return wrap_content(uc, data.ext)
            except Exception:
                return """<a href="/raw/%s">download</a>""" % storage_key

class snippet:
    def GET(self, storage_key, snippet_key):
        batch = Batch.load_most_recent(wrapper)
        data = batch.data_for_storage_key(storage_key)
        return wrap_content(data[snippet_key], data.ext)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
