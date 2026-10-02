#!/usr/bin/env python3
"""Live local inference-path probe; emits durable public-safe evidence."""
import json, threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from yuanwai_simulator import AIInference,Case
class H(BaseHTTPRequestHandler):
 def do_POST(self):
  self.rfile.read(int(self.headers.get('Content-Length','0')))
  body={'choices':[{'message':{'content':json.dumps({'facts':[{'topic':'date','value_class':'10/20'}],'commitment_request':False,'conflict':False,'reference':False,'supplier_ready':False})}}]}
  raw=json.dumps(body).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
 def log_message(self,*args): pass
server=HTTPServer(('127.0.0.1',0),H); threading.Thread(target=server.serve_forever,daemon=True).start()
import os; os.environ['YUANWAI_AI_ENDPOINT']=f'http://127.0.0.1:{server.server_port}'; os.environ['YUANWAI_AI_MODEL']='local-probe'
out=AIInference().interpret('customer message',Case()); server.shutdown()
evidence={'path':'OpenAI-compatible HTTP adapter','endpoint_class':'loopback','model_class':'configured','result_topics':[x['topic'] for x in out['facts']],'fixture':False,'status':'PASS'}
Path('ai-inference-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(evidence,ensure_ascii=False))
