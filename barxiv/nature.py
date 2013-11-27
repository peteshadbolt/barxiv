import re
from datetime import datetime
from time import mktime
import feedparser
from optimize import optimize_search

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_tags(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return title.split('(')[0]
def epoch(dt): return int(mktime(dt.timetuple()))

def get_authors(entry):
    ''' hack to get full author list '''
    s=entry['content'][0]['value']
    start_string='<p>Authors:'
    start=s.find(start_string)
    if start==-1: start=s.find('<p>Author:')
    if start==-1: return 'Author error'
    stop=s.find('</p>', start)
    start+=len(start_string)
    return s[start:stop]

def parse_rss((index, entry)):
    ''' parse a post from the arxiv '''
    if not 'authors' in entry: return None
    section=entry['prism_section']
    allowed=['News & Views', 'Article', 'Letter']
    if not any([section==s for s in allowed]): return None

    out={}
    out['title']=entry['title']
    out['abstract']=entry['summary']
    out['authors']=get_authors(entry)
    out['search']=optimize_search(out['title']+out['abstract']+out['authors'])
    out['link']=entry['link']
    t1=datetime.strptime(entry['prism_publicationdate'], '%Y-%m-%d')
    out['published']='%s' % t1.strftime('%A %d %B')
    out['index']=index
    out['epoch']=epoch(t1)
    return out

def get_all(category=None):
    ''' get the latest n posts from nature as a list of dicts '''
    url_dict={'nature':'http://www.nature.com/nature/journal/vaop/ncurrent/rss.rdf',
                'nphoton':'http://www.nature.com/nphoton/journal/vaop/ncurrent/rss.rdf',
                'nphys':'http://www.nature.com/nphys/journal/vaop/ncurrent/rss.rdf',
                'ncomms':'http://www.nature.com/ncomms/rss/all_index.rdf'}
    feed = feedparser.parse(url_dict[category])
    return list(map(parse_rss, enumerate(feed.entries)))

if __name__=='__main__':
    stuff=get_rss()
