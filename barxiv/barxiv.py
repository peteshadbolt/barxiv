import webapp2
from google.appengine.ext import ndb
import jinja2
import json, time, logging, os, re
import arxiv
import datetime

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

def format_post(post, template, normalization):
    ''' Format a post '''

    # choose the color
    if normalization<1:
        rgb=(245, 245, 245)
    else:
        color=len(post.hits)/float(normalization)
        rgb=map(int, (255*(.8+.2*color), 200, 255*(.9-.5*color)))
        rgb=map(lambda x: min(255, x+30), rgb)

    # if it was posted today, add an image
    image=''
    if (datetime.datetime.today() - post.published).days<1:
        image='<img src="images/today.png">'

    color=''.join(map(chr, rgb)).encode('hex')
    template_values={'image': image,
                     'url': 'http://arxiv.org/pdf/%s' % post.arxiv_id, 
                     'title': post.title, 
                     'arxiv_id': post.arxiv_id, 
                     'short_id': 'p'+post.arxiv_id.replace('.', ''), 
                     'authors': post.authors, 
                     'new': post.published.strftime('%A %d %B'),
                     'abstract': '',
                     'hits': ' '.join(post.hits),
                     'color': color}
    return template.render(template_values)

def build_content(request):
    ''' Builds HTML for the main list of posts ''' 
    # parse the URL
    tags = map(lambda x: x.strip().lower(), request.get('tags').split(','))
    tags = filter(lambda x: len(x)>1, tags)
    sort = str(request.get('nosort'))!='1'

    # get all reccent posts
    query = Post.query(ancestor=post_database_key()).order(-Post.published)
    posts = query.fetch(100)

    # figure out hits
    for post in posts:
        post.hits=[]
        for tag in tags:
            if tag in post.search_terms: post.hits.append(tag)

    # sort
    if sort: posts=sorted(posts, key=lambda x: len(x.hits), reverse=1)

    # build the page
    template = JINJA_ENVIRONMENT.get_template('post.html')
    normalization=max([len(p.hits) for p in posts])
    logging.info(normalization)
    posts=[format_post(post, template, normalization) for post in posts]
    html='\n\n'.join(posts)
    return html

class MainPage(webapp2.RequestHandler):
    def get(self):
        ''' Build the page and send it over '''
        html=build_content(self.request)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        template_values={'all_posts': html}
        self.response.out.write(template.render(template_values))

class InstantPage(webapp2.RequestHandler):
    def get(self):
        ''' Build the page and send it over '''
        html=build_content(self.request)
        self.response.out.write(html)

class AbstractPage(webapp2.RequestHandler):
    def get(self):
        ''' Build the page and send it over '''
        target_id=self.request.get('arxiv_id')
        query = Post.query(Post.arxiv_id==target_id).get() 
        self.response.out.write(query.abstract)

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
    ('/instant', InstantPage),
    ('/abstract', AbstractPage),
    ('/admin/scrape', ScrapePage)], debug=False)


