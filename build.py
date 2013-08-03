import re
import arxiv
import json

cutoff=100

def do_everything():
    ''' load posts, filter them, sort them, and dump to JSON '''
    api_posts=arxiv.get_api(cutoff)
    rss_posts=arxiv.get_rss(cutoff)
    all_posts=api_posts+rss_posts
    all_posts=filter(lambda x: x['repost']==False, all_posts)
    all_posts=sorted(all_posts, key=lambda x: x['epoch'], reverse=True)
    s=json.dumps(all_posts[:cutoff], indent=2)
    f=open('arxiv.json', 'w')
    f.write('var arxivData = '); f.write(s); f.close()

do_everything()

