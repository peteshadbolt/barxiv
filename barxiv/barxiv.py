import webapp2
from google.appengine.ext import ndb
import jinja2
import json, time, logging, os, re
import arxiv

DEFAULT_DATABASE_NAME='BARXIV'
def post_database_key(): return ndb.Key('Post', DEFAULT_DATABASE_NAME)

class Post(ndb.Model):
    ''' Model a post in the database '''
    arxiv_id=ndb.StringProperty()
    title=ndb.TextProperty()
    abstract=ndb.TextProperty()
    authors=ndb.TextProperty()
    search_terms=ndb.StringProperty()
    published=ndb.DateTimeProperty()
    scraped=ndb.DateTimeProperty(auto_now_add=True)

# Set up the templating engine
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):
    def get(self):
        ''' Build the page and send it over '''
        all_posts='posts'

        query = Post.query(ancestor=post_database_key()).order(-Post.published)
        latest_posts = query.fetch(None)

        all_posts=''
        template = JINJA_ENVIRONMENT.get_template('post.html')
        for post in latest_posts:
            template_values={'url': 'http://arxiv.org/pdf/%s' % post.arxiv_id, 
                             'title': post.title, 
                             'authors': post.authors, 
                             'new': post.published.strftime('%A %d %B'),
                             'abstract': 'no abstract'}
            all_posts+=template.render(template_values)

        # Here we build the page based on the URL, for JS-less browsers
        template = JINJA_ENVIRONMENT.get_template('index.html')
        template_values={'all_posts': all_posts}
        self.response.out.write(template.render(template_values))

    # When the user starts typing into the form, they get back sorted JSON objects. 
    # This reduces bandwidth, speeds up page loads, and avoids sorting in JS

class ScrapePage(webapp2.RequestHandler):
    def get(self):
        ''' A cron job said that it's time to scrape the journals '''
        logging.info('Starting scrape')
        summary=''
        number_new=0

        # Put the new posts into the database
        all_posts=arxiv.get_rss()
        for post in all_posts:
            # See if the post is already in the database
            if Post.query(Post.arxiv_id==post.arxiv_id).get()!=None:
                summary+='%s is already in the database<br>' % post.arxiv_id
            else:
                summary+='%s is new, added it to the database<br>' % post.arxiv_id
                db_entry = Post(parent=post_database_key(),  \
                            id=post.arxiv_id,  \
                            arxiv_id=post.arxiv_id, \
                            title=post.title,  \
                            abstract=post.abstract,  \
                            authors=post.authors,  \
                            search_terms=post.search_terms,  \
                            published=post.published)
                number_new+=1
                db_entry.put()

        # Build a little summary page
        summary=('Scraped %d articles. %d new articles added<br>' % (len(all_posts), number_new))+summary
        logging.info('Scraped %d articles. %d new articles added' % (len(all_posts), number_new))
        self.response.out.write(summary)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin/scrape', ScrapePage)], debug=False)


