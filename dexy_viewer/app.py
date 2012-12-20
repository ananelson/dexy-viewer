import web
import os
import dexy.wrapper
import json

urls = (
        '/favicon.ico', 'favicon',
        '/doc/(.*)', 'document',
        '/raw/(.*)', 'raw',
        '/snip/(.*)/(.*)', 'snippet',
        '/(.*)/(.*)', 'grep',
        '/(.*)', 'grep'
        )

render = web.template.render(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../templates'))

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
        print "in grep/GET with expr '%s'" % expr
        wrapper = dexy.wrapper.Wrapper()
        wrapper.setup_read()

        if not expr:
            # Show first 20 records
            rows = wrapper.db.docs(20)
        else:
            # Show whatever matches the query text using sql like %expr% matching
            rows = wrapper.db.query_docs("%%%s%%" % expr)

        artifacts = []

        for row in rows:
            data = wrapper.db.find_filter_artifact_for_doc_key(row['key'])
            if data:
                artifacts.append(data)

        return render.grep(artifacts, expr, keyexpr)

class raw:
    def GET(self, hashstring):
        wrapper = dexy.wrapper.Wrapper()
        wrapper.setup_read()

        data = wrapper.db.find_filter_artifact_for_hashstring(hashstring)
        return data.data()

class document:
    def GET(self, hashstring):
        wrapper = dexy.wrapper.Wrapper()
        wrapper.setup_read()

        data = wrapper.db.find_filter_artifact_for_hashstring(hashstring)

        if data.ext in (".png", ".jpg"): # Add any other image formats here.
            return """<img title="%s" src="/raw/%s" />""" % (data.key, hashstring)
        else:
            try:
                uc = unicode(data)
                json.dumps(uc)
                return wrap_content(uc, data.ext)
            except Exception:
                return """<a href="/raw/%s">download</a>""" % hashstring

class snippet:
    def GET(self, hashstring, snippet_key):
        wrapper = dexy.wrapper.Wrapper()
        wrapper.setup_read()

        data = wrapper.db.find_filter_artifact_for_hashstring(hashstring)
        return wrap_content(data[snippet_key], data.ext)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()

import dexy.utils
