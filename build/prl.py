import re
from datetime import datetime
from time import mktime
import feedparser
from optimize import optimize_search

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_tags(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return title.split('(')[0]

def epoch(dt): return int(mktime(dt.timetuple()))

def get_abstract(summary):
    ''' hack to get full author list '''
    s = summary.split('p>')
    return strip_tags(s[1].strip())[:-2]

def parse_rss((index, entry)):
    ''' parse a post from the arxiv '''
    out={}
    out['title']=entry['title']
    out['abstract']=get_abstract(entry['summary'])
    out['authors']=entry['author']
    out['search']=optimize_search(out['title']+out['abstract']+out['authors'])
    out['link']=entry['link']
    #t1=datetime.strptime(entry['prism_publicationdate'], '%Y-%m-%d')
    t1=datetime.today()
    out['published']='%s' % t1.strftime('%A %d %B')
    out['index']=index
    out['epoch']=epoch(t1)
    return out

def get_all():
    ''' get the latest n posts from nature as a list of dicts '''
    url = 'http://feeds.aps.org/rss/recent/prl.xml'
    feed = feedparser.parse(url)
    return list(map(parse_rss, enumerate(feed.entries)))

if __name__=='__main__':
    stuff=get_rss()
