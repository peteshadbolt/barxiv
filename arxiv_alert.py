import re
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import feedparser 

def strip_authors(html): return re.sub('<[^>]*>', '', html)
def strip_title(title): return title.split('(')[0]

d = feedparser.parse('http://arxiv.org/rss/quant-ph')

keywords=['walk', 'hilbert', 'dimension', 'bosonsampling', 'optics', 'optical', 'photon']
out=open('index.html', 'w')
out.write('<html><head>')
out.write('<link rel="stylesheet" href="css.css" type="text/css">')
out.write('</head><body>')

entries=[]

for entry in d.entries:
    title=entry['title']
    updated='UPDATED' in title
    s=''
    if not updated:
        title=strip_title(title)
        summary=entry['summary']
        authors=strip_authors(entry['author_detail']['name'])
        total=(title+summary+authors).lower()
        matches=[keyword for keyword in keywords if (keyword in total)]
        matches=[' [%s] ' % x for x  in matches]
        if len(matches)>0: s+=('<font color="#cc0000">')
        s+='<b>'+(title)+'</b>'
        s+=('<font size=2pt>'+authors+'  |  '+('  '.join(matches))+'<br><br></font>')
        if len(matches)>0: s+=('</font>')
        entries.append((len(matches), s))

entries=sorted(entries, key=lambda x: x[0], reverse=1)
entries=[x[1] for x in entries]
out.write('\n\n'.join(entries))

out.write('</body></html>')
out.close()


#HandlerClass = SimpleHTTPRequestHandler
#ServerClass  = BaseHTTPServer.HTTPServer
#Protocol     = "HTTP/1.0"
#port = 8000
#server_address = ('127.0.0.1', port)
#HandlerClass.protocol_version = Protocol
#httpd = ServerClass(server_address, HandlerClass)
#sa = httpd.socket.getsockname()
#print "Serving HTTP on", sa[0], "port", sa[1], "..."
#httpd.serve_forever()


    
