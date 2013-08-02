import re
import sys
import feedparser 
import json
from datetime import datetime
from datetime import timedelta
from frequent_words import *

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return title.split('(')[0]

def optimize_search(s):
    ''' optimize a search string, removing common words and duplicates '''
    s=s.lower().replace('\n', ' ')
    s=map(lambda x: x.strip(), list(set(s.split(' '))))
    return ' '.join(filter(lambda x: not x in frequentwords, s))

def parse_arxiv_api((index, entry)):
    ''' parse a post from the arxiv '''
    out={}
    out['title']=entry['title'].replace('\n', '')
    out['abstract']=entry['summary']
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

def parse_arxiv_rss((index, entry)):
    ''' parse a post from the arxiv '''
    out={}
    out['title']=strip_title(entry['title'].replace('\n', ''))
    out['repost']='UPDATED' in entry['title']
    out['abstract']=entry['summary']
    out['authors']=strip_authors(entry['author'])
    out['search']=optimize_search(out['title']+out['abstract']+out['authors'])
    out['link']=entry['link']#.replace('abs', 'pdf')
    t1=datetime.today()
    #out['published']='Published %s ' % (t1.strftime('%A %d %B'))
    out['published']='Today'
    out['index']=index
    out['epoch']=(t1-datetime(1990,1,1)).total_seconds()
    return out

def get_arxiv_api(max_results=100):
    ''' get the latest n posts from the arxiv as a list of dicts '''
    arxiv_api='http://export.arxiv.org/api/query?search_query=cat:quant-ph&start=0&max_results=%d&sortBy=submittedDate&sortOrder=descending' % max_results
    feed = feedparser.parse(arxiv_api)
    return list(map(parse_arxiv_api, enumerate(feed.entries)))

def get_arxiv_rss(max_results=100):
    ''' get the latest n posts from the arxiv as a list of dicts '''
    arxiv_rss='http://arxiv.org/rss/quant-ph'
    feed = feedparser.parse(arxiv_rss)
    return list(map(parse_arxiv_rss, enumerate(feed.entries)))

def do_everything():
    ''' load posts, filter them, sort them, and dump to JSON '''
    api_posts=get_arxiv_api(100)
    rss_posts=get_arxiv_rss(100)
    all_posts=api_posts+rss_posts

    all_posts=filter(lambda x: x['repost']==False, all_posts)

    all_posts=sorted(all_posts, key=lambda x: x['epoch'], reverse=True)

    for post in all_posts:
        print post['title'].encode('ascii', 'ignore')
        print

    s=json.dumps(all_posts[:100], indent=2)
    f=open('arxiv.json', 'w')
    f.write('var arxivData = '); f.write(s); f.close()

do_everything()

