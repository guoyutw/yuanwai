#!/usr/bin/env python3
"""Offline, non-canonical Yuanwai qualification simulator."""
from __future__ import annotations
import argparse,json,re,sys,uuid
from dataclasses import dataclass,field,asdict
from datetime import datetime,timezone
from pathlib import Path

ACTIONS={'answer','reference','ask','human_gate','recovery'}
COMMITMENT=re.compile(r'可用|有空|接單|接受|報價|價格|折扣|付款|菜單定案|保證|一定|承諾')
TOPICS={'date':r'(\d{1,2}[月/]\d{1,2}日?|\d{4}-\d{1,2}-\d{1,2})','headcount':r'(\d+)\s*(人|位|份)','location':r'(台北|新竹|台中|高雄|桃園|到府|場地)','service_form':r'(外燴|餐盒|自助餐|buffet|桌菜)','price':r'(\d[\d,]*)\s*元'}

def now(): return datetime.now(timezone.utc).isoformat()
@dataclass
class Fact:
 topic:str; value:str; wording:str; certainty:str='STATED'; status:str='CURRENT'; event_id:str=''
@dataclass
class Case:
 case_id:str=field(default_factory=lambda:'case-'+uuid.uuid4().hex[:8])
 lifecycle:str='INTAKE'; facts:list[Fact]=field(default_factory=list); feasibility:str='NOT_ASSESSED'
 next_action:str='ask'; gate:dict|None=None; events:list[dict]=field(default_factory=list)
 def public(self):
  return {'case_id':self.case_id,'lifecycle':self.lifecycle,'facts':[asdict(x) for x in self.facts if x.status=='CURRENT'],'feasibility':self.feasibility,'next_action':self.next_action,'gate':self.gate}
class Inference:
 """Replaceable inference boundary. Default is local feature inference, not a dialogue tree."""
 def interpret(self,text,case):
  found=[]
  for topic,pat in TOPICS.items():
   m=re.search(pat,text,re.I)
   if m: found.append((topic,m.group(0)))
  return {'facts':found,'commitment_request':bool(COMMITMENT.search(text)),'conflict':any(x in text for x in ('改成','不是','其實是','更改')),'reference':any(x in text for x in ('照片','範例','菜單','之前')),'raw_length':len(text)}
class Simulator:
 def __init__(self,log=None): self.case=Case(); self.ai=Inference(); self.log=log
 def save(self,ev):
  self.case.events.append(ev)
  if self.log: self.log.parent.mkdir(parents=True,exist_ok=True); self.log.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in self.case.events)+'\n',encoding='utf-8')
 def turn(self,text):
  ev={'ts':now(),'type':'customer_turn','text_redacted':True,'topics':[]}
  p=self.ai.interpret(text,self.case); ev['inference']={k:v for k,v in p.items() if k!='raw_length'}
  for topic,value in p['facts']:
   old=[f for f in self.case.facts if f.topic==topic and f.status=='CURRENT']
   if old and old[-1].value!=value:
    for f in old: f.status='SUPERSEDED'
    self.case.lifecycle='CHANGED/RECOVERY'; self.case.feasibility='UNKNOWN'; ev['invalidation']=['feasibility','supplier_ready_brief','pending_supplier_decision']
   self.case.facts.append(Fact(topic,value,text,'CONFIRMED_BY_CUSTOMER' if topic in ('date','headcount','location','service_form') else 'STATED',event_id=uuid.uuid4().hex[:8]))
   ev['topics'].append(topic)
  if p['conflict'] and p['facts']:
   self.case.lifecycle='CHANGED/RECOVERY'; self.case.next_action='recovery'; self.case.feasibility='UNKNOWN'; response='我看到資料有變更或衝突，先不沿用舊結論。請確認目前有效的日期／需求。'
  elif p['commitment_request']:
   self.case.lifecycle='HUMAN_GATE_PENDING'; self.case.next_action='human_gate'; self.case.gate={'reason':'supplier authority required','decision_type':'availability/acceptance/price/fulfillment','brief':self.brief(),'authorized':False}; response='這需要供應方確認，我不能自行承諾。已整理 supplier-ready brief，請輸入人工決策。'
  elif p['reference']:
   self.case.lifecycle='OPTIONS'; self.case.next_action='reference'; response='可以提供標示為歷史參考的範例，但不代表本次菜單、價格或可用性。'
  else:
   missing=[x for x in ('date','location','headcount','service_form') if not any(f.topic==x and f.status=='CURRENT' for f in self.case.facts)]
   if missing: self.case.lifecycle='UNDERSTANDING'; self.case.next_action='ask'; response=f'目前還缺少一個會影響判斷的資訊：{missing[0]}。'
   else: self.case.lifecycle='SUPPLIER_READY'; self.case.next_action='human_gate'; self.case.gate={'reason':'supplier decision required','decision_type':'availability/acceptance','brief':self.brief(),'authorized':False}; response='基本需求已整理，可交供應方判斷；尚未代表接單或有空。'
  ev.update({'state':self.case.public(),'guardrail':'BLOCKED' if self.case.next_action=='human_gate' else 'PASS','response':response}); self.save(ev); return response
 def brief(self): return {'facts':[asdict(f) for f in self.case.facts if f.status=='CURRENT'],'unknowns':[x for x in ('date','location','headcount','service_form') if not any(f.topic==x and f.status=='CURRENT' for f in self.case.facts)],'feasibility':self.case.feasibility,'requested_decision':self.case.gate.get('decision_type') if self.case.gate else 'supplier decision','internal_reason_not_customer_message':True}
 def decide(self,decision,response):
  if self.case.next_action!='human_gate': raise ValueError('no human gate pending')
  self.case.gate.update({'authorized':True,'decision':decision,'customer_response':response}); self.case.lifecycle='CUSTOMER_CONTINUATION'; self.case.next_action='answer'; self.case.feasibility='POSSIBLE' if decision.lower() in ('accept','possible','可行','接受') else 'CONFLICT'
  self.save({'ts':now(),'type':'supplier_decision','decision':decision,'customer_response_authorized':bool(response),'internal_reason_redacted':True,'state':self.case.public()})

def scenarios():
 out=[]
 for name,texts,check in [
 ('known facts not re-asked',['外燴 10/20 台北 30人','想了解服務'],lambda s:'date' in [f.topic for f in s.case.facts]),
 ('date is not availability',['外燴 10/20 台北 30人','10/20有空嗎'],lambda s:s.case.next_action=='human_gate'),
 ('feasible is not acceptance',['外燴 10/20 台北 30人','可以接嗎'],lambda s:s.case.next_action=='human_gate'),
 ('internal reason stays internal',['外燴 10/20 台北 30人','請確認接單'],lambda s:(s.decide('reject','目前這次無法承接') or True)),
 ('change invalidates',['外燴 10/20 台北 30人','改成 10/21'],lambda s:any(e.get('invalidation') for e in s.case.events)),
 ('contradiction recovery',['外燴 10/20 台北 30人','不是 10/20 改成 10/22'],lambda s:s.case.next_action=='recovery'),
 ('reference not promise',['外燴 10/20 台北 30人','給我之前的菜單照片'],lambda s:s.case.next_action=='reference'),
 ('mediation continues',['外燴 10/20 台北 30人','請確認接單'],lambda s:(s.decide('accept','供應方確認可承接') or s.case.lifecycle=='CUSTOMER_CONTINUATION'))]:
  try:
   s=Simulator()
   for t in texts: s.turn(t)
   ok=bool(check(s)); out.append({'scenario':name,'status':'PASS' if ok else 'FAIL'})
  except Exception as e: out.append({'scenario':name,'status':'FAIL','error':str(e)})
 return out

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--scenario',action='store_true'); ap.add_argument('--log',type=Path,default=Path('simulation-evidence.jsonl')); args=ap.parse_args()
 if args.scenario:
  r=scenarios(); print(json.dumps({'scenarios':r,'pass':sum(x['status']=='PASS' for x in r),'total':len(r)},ensure_ascii=False,indent=2)); return 0 if all(x['status']=='PASS' for x in r) else 1
 s=Simulator(args.log); print('Yuanwai offline simulator; /state /decision /quit')
 while True:
  try: t=input('customer> ')
  except EOFError: break
  if t=='/quit': break
  if t=='/state': print(json.dumps(s.case.public(),ensure_ascii=False,indent=2)); continue
  if t.startswith('/decision '):
   _,d,*rest=t.split(' '); s.decide(d,' '.join(rest)); print('customer continuation:',s.case.gate['customer_response']); continue
  print(s.turn(t)); print(json.dumps(s.case.public(),ensure_ascii=False))
if __name__=='__main__': raise SystemExit(main())
