import re
from datetime import datetime
from time import mktime
import feedparser
from optimize import optimize_search

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_tags(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return re.sub('\[[^\]]*\]', '', title).strip()

def epoch(dt): return int(mktime(dt.timetuple()))

def split_authors(s):
    ''' hack to get full author list '''
    start_string='Authors:'
    start=s.find(start_string)
    if start==-1: 
        start_string='Author:'
        start=s.find(start_string)

    if start==-1: return 'error', 'error'
    stop=len(s)
    start+=len(start_string)
    return strip_tags(s[:start-len(start_string)]), s[start:stop]

def parse_rss((index, entry)):
    ''' parse a post from science '''
    allowed=['[Research Article]', '[Report]']
    if not any([entry['title'].startswith(x) for x in allowed]): return None

    out={}
    out['title']=strip_title(entry['title'])
    out['abstract'], out['authors']=split_authors(entry['summary'])
    out['search']=optimize_search(out['title']+out['abstract']+out['authors'])
    out['link']=entry['link']
    #t1=datetime.strptime(entry['prism_publicationdate'], '%Y-%m-%d')
    #out['published']='%s' % t1.strftime('%A %d %B')
    out['published']='New'
    out['index']=index
    #out['epoch']=epoch(t1)
    out['epoch']=0
    return out

def get_rss(url):
    ''' get the latest n posts from nature as a list of dicts '''
    feed = feedparser.parse(url)
    return list(map(parse_rss, enumerate(feed.entries)))

def get_all(category=None):
    ''' get both the current and express feeds '''
    normal=get_rss('http://www.sciencemag.org/rss/current.xml')
    express=get_rss('http://www.sciencemag.org/rss/express.xml')
    return express+normal

if __name__=='__main__':
    stuff=get_all()
