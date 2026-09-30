"""Standalone local JSON comparator. No database, models or paid APIs."""
import argparse
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from json_compare import compare

ROOT=Path(__file__).resolve().parent

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def send(self,status,value,kind='application/json'):
        if not isinstance(value,bytes):value=json.dumps(value,ensure_ascii=False).encode('utf-8')
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8')
        self.send_header('Content-Length',str(len(value)));self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'")
        self.end_headers();self.wfile.write(value)
    def permitted(self):
        if self.headers.get('Host') not in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'):
            self.send(403,{'error':'Invalid host'});return False
        origin=self.headers.get('Origin')
        if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):
            self.send(403,{'error':'Cross-origin blocked'});return False
        return True
    def do_GET(self):
        if not self.permitted():return
        routes={'/':('index.html','text/html'),'/assets/style.css':('style.css','text/css'),'/assets/json-product.js':('json-product.js','text/javascript')}
        if self.path=='/health':return self.send(200,{'ok':True,'product':'json-compare-portable'})
        if self.path not in routes:return self.send(404,{'error':'Not found'})
        name,kind=routes[self.path];self.send(200,(ROOT/name).read_bytes(),kind)
    def do_POST(self):
        if not self.permitted():return
        if self.path!='/venture/json-compare/api/compare':return self.send(404,{'error':'Not found'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=1048576:raise ValueError('Request too large or empty')
            if 'application/json' not in self.headers.get('Content-Type',''):raise ValueError('JSON request required')
            data=json.loads(self.rfile.read(size))
            if not isinstance(data,dict):raise ValueError('Object required')
            result=compare(data.get('left'),data.get('right'),data.get('ignore_paths'),data.get('unordered') is True)
            self.send(200,result)
        except (ValueError,TypeError,RecursionError):self.send(400,{'error':'Invalid JSON, options, size or nesting. Check your inputs.'})

if __name__=='__main__':
    args=argparse.ArgumentParser();args.add_argument('--port',type=int,default=0);args.add_argument('--no-browser',action='store_true');options=args.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',options.port),Handler)
    print(f'http://127.0.0.1:{server.server_port}/',flush=True)
    if not options.no_browser:threading.Timer(.3,lambda:webbrowser.open(f'http://127.0.0.1:{server.server_port}/')).start()
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
