import re
from datetime import datetime
from datetime import timedelta
from frequent_words import *
import feedparser

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_tags(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return title.split('(')[0]

def optimize_search(s):
    ''' optimize a search string, removing common words and duplicates '''
    s=s.lower().replace('\n', ' ')
    s=map(lambda x: x.strip(), list(set(s.split(' '))))
    return ' '.join(filter(lambda x: not x in frequentwords, s))

def parse_api((index, entry)):
    ''' parse a post from the arxiv '''
    out={}
    out['title']=entry['title'].replace('\n', '')
    out['abstract']=strip_tags(entry['summary'])
    out['authors']=', '.join(map(lambda x: x['name'], entry['authors']))
    out['search']=optimize_search(out['title']+out['abstract']+out['authors'])
    out['link']=entry['link']#.replace('abs', 'pdf')
    t1=datetime.strptime(entry['published'].split('T')[0], '%Y-%m-%d')
    t2=datetime.strptime(entry['updated'].split('T')[0], '%Y-%m-%d')
    out['published']='%s' % t2.strftime('%A %d %B')
    out['index']=index
    out['epoch']=(t2-datetime(1990,1,1)).total_seconds()
    out['repost']=not t2==t1
    return out

def parse_rss((index, entry)):
    ''' parse a post from the arxiv '''
    out={}
    out['title']=strip_title(entry['title'].replace('\n', ''))
    out['repost']='UPDATED' in entry['title']
    out['abstract']=strip_tags(entry['summary'])
    out['authors']=strip_authors(entry['author'])
    out['search']=optimize_search(out['title']+out['abstract']+out['authors'])
    out['link']=entry['link']#.replace('abs', 'pdf')
    t1=datetime.today()
    out['published']='Today'
    out['index']=index
    out['epoch']=(t1-datetime(1990,1,1)).total_seconds()
    return out

def get_api(max_results=100):
    ''' get the latest n posts from the arxiv as a list of dicts '''
    api='http://export.arxiv.org/api/query?search_query=cat:quant-ph&start=0&max_results=%d&sortBy=submittedDate&sortOrder=descending' % max_results
    feed = feedparser.parse(api)
    return list(map(parse_api, enumerate(feed.entries)))

def get_rss(max_results=100):
    ''' get the latest n posts from the arxiv as a list of dicts '''
    rss='http://arxiv.org/rss/quant-ph'
    feed = feedparser.parse(rss)
    return list(map(parse_rss, enumerate(feed.entries)))
