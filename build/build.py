import codecs
import time
import json
import arxiv
import nature
import science
from ftplib import FTP

cutoff=100

def trim_authors(post, chop=300):
    if len(post['authors'])>chop:
        post['authors']=post['authors'][:chop]+'...'
    return post

def generate_json(source, name):
    ''' load posts, filter them, sort them, and dump to JSON '''
    print 'caching %s...' % name
    all_posts=source.get_all(name)
    all_posts=filter(lambda x: x!=None, all_posts)
    all_posts=sorted(all_posts, key=lambda x: x['epoch'], reverse=True)
    all_posts=map(trim_authors, all_posts)
    s=json.dumps(all_posts[:cutoff], indent=2)
    f=open('../%s.json' % name, 'w')
    f.write(s)
    f.close()

def upload():
    ''' upload all the jsons '''
    print 'uploading...'
    ftp = FTP('peteshadbolt.co.uk')
    ftp.login('peteshad', 'ah_1one')
    print 'logged in to FTP ok'
    ftp.cwd('public_html/barxiv')

    for file in ['nature', 'science', 'quant-ph', 'nphoton', 'nphys', 'ncomms']:
        file='%s.json' % file
        print file
        ftp.storlines('STOR '+file, open('../'+file))

    file='index.html'
    ftp.storlines('STOR '+file, open('../'+file))

    ftp.quit()
    print 'done'

def get_post(entry):
    post=''
    post+='<div class="post" style="background-color: #eeeeff;">'
    post+='<div>'
    post+='<a href="' + entry['link'] + '" target="_blank">' + entry['title'] + '</a>'
    post+='<br class="clear"/>'
    post+='</div>'
    post+='<div>'
    post+='<div class="authors">'+entry['authors']+'</div>'
    if entry['published']=='New':
        post+='<div class="newPost">'+entry['published']+'</div>'
    else :
        post+='<div class="date">'+entry['published']+'</div>'
    post+='<br class="clear"/>'
    post+='</div>'
    #post+='<div class="abstract" style="display: none;">'+entry.abstract+'</div>'
    post+='</div>'
    return post

def rewrite_html():
    ''' rewrite the html for javascript-less browsers '''
    qp=json.loads(open('../quant-ph.json').read())
    post_text='\n'.join(map(get_post, qp))
    template=open('template.html', 'r').read()
    template=template.replace('<!--AAAAAAAAAAAAAAAAA-->', post_text)
    #f=open('../index.html', 'w')
    f=codecs.open('../index.html', encoding='utf-8', mode='w')
    f.write(template)
    f.close()
    print 'wrote passive html'

def do_everything():
    ''' just flipping well do everything '''
    #generate_json(arxiv, 'quant-ph')
    #generate_json(science, 'science')
    #generate_json(nature, 'nature')
    #generate_json(nature, 'nphoton')
    #generate_json(nature, 'nphys')
    #generate_json(nature, 'ncomms')
    #generate_json(prl, 'prl')
    rewrite_html()
    upload()

minutes=30

while True:
    do_everything()
    for i in range(60*minutes):
        time.sleep(1)

