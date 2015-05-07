#!/usr/bin/env python
import os
import jinja2
import webapp2
from random import randint


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("index.html")


class LotoHandler(BaseHandler):
    def get(self):
        loto = []
        while len(loto) != 8:
            loto.append(randint(1, 39))
        params = {"loto": loto}
        self.render_template("loto.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/loto', LotoHandler)
], debug=True)
