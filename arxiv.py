import re
import sys
import feedparser 
import json

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return title.split('(')[0]

def parse_arxiv_post((index, entry)):
    ''' parse a post from the arxiv '''
    out={}
    out['title']=entry['title'].replace('\n', '')
    out['abstract']=entry['summary']
    out['authors']=', '.join(map(lambda x: x['name'], entry['authors']))
    out['search']=(out['title']+out['abstract']+out['authors']).lower().replace('\n', ' ')
    out['link']=entry['link']#.replace('abs', 'pdf')
    out['published']=entry['published']
    out['source']='arxiv'
    out['index']=index
    return out

def get_arxiv(max_results=30):
    ''' get the latest n posts from the arxiv as a list of dicts '''
    arxiv_api='http://export.arxiv.org/api/query?search_query=cat:quant-ph&start=0&max_results=%d&sortBy=submittedDate&sortOrder=descending' % max_results
    arxiv_rss='http://arxiv.org/rss/quant-ph'
    feed = feedparser.parse(arxiv_api)
    return list(reversed(map(parse_arxiv_post, enumerate(feed.entries))))

def save_arxiv(d):
    ''' save the arxiv as json '''
    s=json.dumps(d, indent=2)
    f=open('arxiv.json', 'w')
    f.write('var arxivData = ')
    f.write(s)
    f.close()

d=get_arxiv(10)
for item in d:
    print item['published']
save_arxiv(d)

