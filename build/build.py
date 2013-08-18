import sched, time
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
        file='../%s.json' % file
        print file
        ftp.storlines('STOR '+file, open(file))
    ftp.quit()
    print 'done'

def do_everything():
    ''' just flipping well do everything '''
    #try: 
    generate_json(arxiv, 'quant-ph')
    generate_json(science, 'science')
    generate_json(nature, 'nature')
    generate_json(nature, 'nphoton')
    generate_json(nature, 'nphys')
    generate_json(nature, 'ncomms')
    #generate_json(prl, 'prl')
    upload()
    #except:
        #print 'error!'


minutes=30

while True:
    do_everything()
    for i in range(60*minutes):
        time.sleep(1)

