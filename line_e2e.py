#!/usr/bin/env python3
"""Bounded synthetic LINE adapter for Yuanwai Issue #75.

Live LINE credentials are supplied only through environment variables; no values are persisted.
"""
import argparse, base64, hashlib, hmac, json, os, secrets, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from yuanwai_simulator import Simulator

ROOT=Path(os.environ.get('YUANWAI_LINE_STATE_DIR','line-state'))

def digest(value): return hashlib.sha256(value.encode()).hexdigest()[:16]
def case_id(user_id): return 'line-'+digest(user_id)

def verify_signature(body, signature, secret):
    expected=base64.b64encode(hmac.new(secret.encode(), body, hashlib.sha256).digest()).decode()
    return bool(signature) and hmac.compare_digest(expected, signature)

class LineTransport:
    def __init__(self, channel_secret=None, access_token=None, reply_url=None):
        self.secret=channel_secret or os.environ.get('LINE_CHANNEL_SECRET')
        self.token=access_token or os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
        self.reply_url=reply_url or os.environ.get('LINE_REPLY_URL','https://api.line.me/v2/bot/message/reply')
    def reply(self, reply_token, text):
        if not self.token: raise RuntimeError('LINE access token unavailable; HOLD')
        req=urllib.request.Request(self.reply_url,data=json.dumps({'replyToken':reply_token,'messages':[{'type':'text','text':text}],}).encode(),headers={'Authorization':'Bearer '+self.token,'Content-Type':'application/json'},method='POST')
        with urllib.request.urlopen(req,timeout=30) as r: return r.status
    def push(self, user_id, text):
        if not self.token: raise RuntimeError('LINE access token unavailable; HOLD')
        req=urllib.request.Request('https://api.line.me/v2/bot/message/push',data=json.dumps({'to':user_id,'messages':[{'type':'text','text':text}]}).encode(),headers={'Authorization':'Bearer '+self.token,'Content-Type':'application/json'},method='POST')
        with urllib.request.urlopen(req,timeout=30) as r: return r.status

class LineBridge:
    def __init__(self, state_dir=ROOT, transport=None):
        self.root=Path(state_dir); self.root.mkdir(parents=True,exist_ok=True); self.transport=transport or LineTransport()
    def process(self, user_id, text, reply_token=None, event_id=None, deliver=True):
        cid=case_id(user_id); path=self.root/(cid+'.json'); sim=Simulator(path,False)
        response=sim.turn(text)
        if sim.case.next_action=='ask':
            inference=sim.case.events[-1].get('inference',{}) if sim.case.events else {}
            unknowns=inference.get('unknowns',[])
            if unknowns:
                response='請問'+str(unknowns[0]).rstrip('？?')+'？'
        result={'event_id_hash':digest(event_id or secrets.token_hex(8)),'user_id_hash':digest(user_id),'case_id':cid,'next_action':sim.case.next_action,'lifecycle':sim.case.lifecycle,'reply_authorized':sim.case.next_action!='human_gate','outbound_status':'NOT_SENT'}
        if deliver and reply_token:
            if sim.case.next_action=='human_gate': result['outbound_status']='GATE_HOLD'
            else: result['outbound_status']='SENT'; result['transport_status']=self.transport.reply(reply_token,response)
        (self.root/(cid+'.evidence.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        return response,result
    def operator_decision(self,user_id, decision, internal_reason, outward_response, deliver=True):
        path=self.root/(case_id(user_id)+'.json'); sim=Simulator(path,False)
        response=sim.decide(decision,internal_reason,outward_response)
        if deliver: self.transport.push(user_id,response)
        return response,sim
    def handle_webhook(self, payload, signature, deliver=True):
        raise RuntimeError('Use handle_raw_webhook with exact raw body bytes')
    def handle_raw_webhook(self, body, signature, deliver=True):
        if not self.transport.secret or not verify_signature(body,signature,self.transport.secret): raise RuntimeError('LINE signature invalid; HOLD')
        payload=json.loads(body)
        receipts=[]
        for event in payload.get('events',[]):
            if event.get('type')!='message' or event.get('message',{}).get('type')!='text': continue
            user=event.get('source',{}).get('userId'); text=event['message']['text']; token=event.get('replyToken')
            _,receipt=self.process(user,text,token, event.get('webhookEventId'),deliver); receipts.append(receipt)
        return receipts
    def public_evidence(self,user_id):
        cid=case_id(user_id); sim=Simulator(self.root/(cid+'.json'),False)
        return {'case_id':cid,'state':sim.case.public(safe=True),'events':[({**{k:v for k,v in e.items() if k not in ('inference', 'state')},'state':sim.case.public(safe=True)} if 'state' in e else {k:v for k,v in e.items() if k not in ('inference',)}) for e in sim.case.events]}

def webhook_server(bridge, host='127.0.0.1', port=8080):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            n=int(self.headers.get('Content-Length','0')); body=self.rfile.read(n)
            try:
                bridge.handle_raw_webhook(body,self.headers.get('X-Line-Signature',''),True); self.send_response(200)
            except Exception: self.send_response(400)
            self.end_headers()
        def log_message(self,*args): return
    return HTTPServer((host,port),Handler)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--synthetic',action='store_true'); ap.add_argument('--serve',action='store_true'); ap.add_argument('--port',type=int,default=8080); ap.add_argument('--state-dir',default=str(ROOT)); a=ap.parse_args()
    if a.serve: webhook_server(LineBridge(a.state_dir),port=a.port).serve_forever()
    if not a.synthetic: raise SystemExit('Use --synthetic for bounded local test; live webhook requires LINE credentials and tunnel.')
    bridge=LineBridge(a.state_dir); user='synthetic-owner-line-user';
    first,_=bridge.process(user,'10/20 中壢 約30人 歐式自助餐',deliver=False)
    assert first.endswith('？') and first.count('？')==1
    bridge.process(user,'所以 10/20 你們能承作嗎？',deliver=False)
    hold=bridge.public_evidence(user); assert hold['state']['next_action']=='human_gate'
    _, decision_case=bridge.operator_decision(user,'accept','synthetic private reason','我們確認 10/20 可以承作。',deliver=False)
    assert decision_case.case.lifecycle=='CUSTOMER_CONTINUATION'
    response,after=bridge.process(user,'謝謝，請繼續確認細節',deliver=False)
    ev=bridge.public_evidence(user); raw=json.dumps(ev,ensure_ascii=False); assert 'synthetic private reason' not in raw and '10/20' not in raw
    out={'fixture':False,'synthetic':True,'case_id':case_id(user),'same_case':after['case_id']==case_id(user),'gate_hold':hold['state']['next_action']=='human_gate','authorized_continuation':decision_case.case.lifecycle=='CUSTOMER_CONTINUATION','public_safe':True,'outbound_authorized_response_hash':digest('我們確認 10/20 可以承作。')}
    Path('line-e2e-evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
