import re
import json
import arxiv
import nature

cutoff=100

def trim_authors(post, chop=300):
    if len(post['authors'])>chop:
        post['authors']=post['authors'][:chop]+'...'
    return post

def do_arxiv():
    ''' load posts, filter them, sort them, and dump to JSON '''
    print 'caching quant-ph...'
    all_posts=arxiv.get_all()
    all_posts=filter(lambda x: x!=None, all_posts)
    all_posts=sorted(all_posts, key=lambda x: x['epoch'], reverse=True)
    all_posts=map(trim_authors, all_posts)
    s=json.dumps(all_posts[:cutoff], indent=2)
    f=open('../quant-ph.json', 'w')
    f.write(''); f.write(s); f.close()

def do_nature(url, filename):
    ''' load posts, filter them, sort them, and dump to JSON '''
    print 'caching %s...' % filename
    all_posts=nature.get_rss(url)
    all_posts=filter(lambda x: x!=None, all_posts)
    all_posts=sorted(all_posts, key=lambda x: x['epoch'], reverse=True)
    all_posts=map(trim_authors, all_posts)
    s=json.dumps(all_posts[:cutoff], indent=2)
    f=open('../%s.json' % filename, 'w')
    f.write(''); f.write(s); f.close()

do_arxiv()
do_nature('http://www.nature.com/nature/journal/vaop/ncurrent/rss.rdf', 'nature')
do_nature('http://www.nature.com/nphoton/journal/vaop/ncurrent/rss.rdf', 'nphoton')
do_nature('http://www.nature.com/nphys/journal/vaop/ncurrent/rss.rdf', 'nphys')
do_nature('http://www.nature.com/ncomms/rss/all_index.rdf', 'ncomms')

