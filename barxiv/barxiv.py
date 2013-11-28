import webapp2
from google.appengine.ext import ndb
import jinja2
import json, time, logging, os, re
import arxiv

DEFAULT_DATABASE_NAME='BARXIV'
def post_database_key(): return ndb.Key('Post', DEFAULT_DATABASE_NAME)

class post(ndb.Model):
    ''' Model a post in the database '''
    token=ndb.StringProperty()
    name=ndb.StringProperty()
    email=ndb.StringProperty()
    intent=ndb.StringProperty()
    state=ndb.StringProperty()
    duration=ndb.IntegerProperty()
    date=ndb.DateTimeProperty(auto_now_add=True)
    started=ndb.DateTimeProperty()

# Set up the templating engine
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class ScrapePage(webapp2.RequestHandler):
    def get(self):
        ''' Time to scrape the journals '''
        logging.info('Starting scrape')
        all_posts=arxiv.get_rss()
        for post in all_posts:
            continue
            token = accessToken(parent=access_token_database_key())
            # build the token here
            token.put()

class MainPage(webapp2.RequestHandler):
    def get(self):
        ''' Build the page and send it over '''
        template = JINJA_ENVIRONMENT.get_template('index.html')
        template_values={}
        self.response.out.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin/scrape', ScrapePage)], debug=False)


