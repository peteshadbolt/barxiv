import re
import webapp2
import json, time, logging, os
import jinja2
import codecs
import arxiv
import nature
import science

# Set up the templating engine
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

cutoff=100

def trim_authors(post, chop=300):
    ''' Get rid of this '''
    if len(post['authors'])>chop:
        post['authors']=post['authors'][:chop]+'...'
    return post

def scrape_site(source, name):
    ''' load posts, filter them, sort them, and dump to JSON '''
    # this should write to a datastore
    # we should use hashes to identify unique posts to the arxiv
    all_posts=source.get_all(name)
    all_posts=filter(lambda x: x!=None, all_posts)
    all_posts=sorted(all_posts, key=lambda x: x['epoch'], reverse=True)
    all_posts=map(trim_authors, all_posts)
    s=json.dumps(all_posts[:cutoff], indent=2)
    logging.info(s)
    #f=open('cache/%s.json' % name, 'w')
    #f.write(s)
    #f.close()

class MainPage(webapp2.RequestHandler):
    def get(self):
        ''' Build the page and send it over '''
        # Construct a string detailing the access token state
        #access_token_state=database.check_token(self.request.get('accessToken').strip())

        # Template the page and send it back to the user
        template = JINJA_ENVIRONMENT.get_template('index.html')
        #template_values={'access_token_message': access_token_state['message']}
        template_values={}
        self.response.out.write(template.render(template_values))

class GetChipPage(webapp2.RequestHandler):
    def get(self):
        ''' User asked for a chip '''
        chip = self.request.get('chipName')
        chip_json = chip_library.chip_data[chip]
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.dumps(chip_json))

class ScrapePage(webapp2.RequestHandler):
    def get(self):
        ''' Time to scrape the journals '''
        logging.info('Starting scrape')
        scrape_site(arxiv, 'quant-ph')
        scrape_site(science, 'science')
        scrape_site(nature, 'nature')
        scrape_site(nature, 'nphoton')
        scrape_site(nature, 'nphys')
        scrape_site(nature, 'ncomms')
        logging.info('Scrape done')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/chip', GetChipPage),
    ('/admin/scrape', ScrapePage),
], debug=False)

