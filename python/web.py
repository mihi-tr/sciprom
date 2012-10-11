import BaseHTTPServer
import unidecode
from pubmed import Pubmed
import json,re
import urlparse
import beaker.cache

cache=beaker.cache.CacheManager()

def slugify(str):
  str = unidecode.unidecode(str).lower()
  return re.sub(r'\W+','-',str)

def convert_articles(articles):
  return [convert_article(a) for a in articles]

def convert_article(article):
  return {"PMID":article["PMID"], "authors":
    [convert_author(a) for a in article["authors"]]}

def convert_author(author):
  name="%s %s"%(author["ForeName"],author["LastName"])
  return {"Name":name,
    "slug":slugify(name)}

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  
  def do_GET(self):
    tc=cache.get_cache(slugify(self.path),expire=43200)
    self.send_response(200,"All fine")
    self.send_header("Content-type","application/json")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    articles=tc.get(key="articles",createfunc=self.process)
    self.wfile.write(articles)
  
  def process(self):
    params=urlparse.parse_qs(urlparse.urlparse(self.path).query)
    pm=Pubmed("mihi@tentacleriot.eu")
    pm.query(params["query"])
    pm.fetch()
    pm.parse()
    return json.dumps(convert_articles(pm.articles))
    

if __name__=="__main__":
  httpd=BaseHTTPServer.HTTPServer(('127.0.0.1',9876),RequestHandler)
  httpd.serve_forever()


