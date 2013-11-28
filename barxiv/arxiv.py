import re
from datetime import datetime
from time import mktime
import feedparser
from optimize import optimize_search

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_tags(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return title.split('(')[0]
def epoch(dt): return int(mktime(dt.timetuple()))

class post:
    def __init__(self, entry):
        ''' A post on the arxiv '''
        self.arxiv_id=entry['id'].split('/')[-1]
        self.title=strip_title(entry['title'].replace('\n', ''))
        self.abstract=strip_tags(entry['summary'])
        self.authors=strip_authors(entry['author'])
        self.search_terms=optimize_search(self.title+self.abstract+self.authors)
        self.pdf_url=entry['link'].replace('abs', 'pdf')
        t1=datetime.today()
        self.published_epoch=epoch(t1)

    def __str__(self):
        ''' Convert to string '''
        return '%s: %s' % (self.arxiv_id, self.title)

def get_rss():
    ''' get the latest n posts from the arxiv as a list of dicts '''
    rss_url='http://arxiv.org/rss/quant-ph'
    feed = feedparser.parse(rss_url)
    posts = list(map(post, feed.entries))
    return posts

#def get_api():
    #''' get the latest n posts from the arxiv as a list of dicts '''
    #api='http://export.arxiv.org/api/query?search_query=cat:quant-ph&start=0&max_results=%d&sortBy=submittedDate&sortOrder=descending' % max_results
    #feed = feedparser.parse(api)
    #return list(map(parse_api, enumerate(feed.entries)))

#def parse_api((index, entry)):
    #''' parse a post from the arxiv '''
    #out={}
    #out['title']=entry['title'].replace('\n', '')
    #out['id']=entry['id']
    #out['abstract']=strip_tags(entry['summary'])
    #out['authors']=', '.join(map(lambda x: x['name'], entry['authors']))
    #out['search']=optimize_search(out['title']+out['abstract']+out['authors'])
    #out['link']=entry['link'].replace('abs', 'pdf')
    #t1=datetime.strptime(entry['published'].split('T')[0], '%Y-%m-%d')
    #t2=datetime.strptime(entry['updated'].split('T')[0], '%Y-%m-%d')
    #out['published']='%s' % t2.strftime('%A %d %B')
    #out['index']=index
    #out['epoch']=epoch(t2)
    #if not t2==t1: return None
    #return out


#def get_all(category=None):
    #''' get all posts from the arxiv '''
    #api_posts=get_api()
    #rss_posts=list(reversed(get_rss()))
    #posts=rss_posts+api_posts
    #posts=filter(lambda x: x!=None, posts)

     #remove dupicates
    #unique_posts=[]
    #used_ids=[]
    #for post in posts:
        #ft=strip_tags(post['title'].lower()).replace(' ', '').replace('.', '').strip()
        #if not ft in used_ids:
            #unique_posts.append(post)
            #used_ids.append(ft)

    #unique_posts=filter(lambda x: x!=None, unique_posts)
    #return unique_posts

#if __name__=='__main__':
    #posts=get_all()

