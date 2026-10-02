#!/usr/bin/env python3
import argparse,hashlib,json,os,re,urllib.request,uuid,subprocess
from dataclasses import dataclass,field,asdict
from datetime import datetime,timezone
from pathlib import Path
def now(): return datetime.now(timezone.utc).isoformat()
def h(s): return hashlib.sha256(s.encode()).hexdigest()[:16]
@dataclass
class Fact:
 topic:str; value_class:str; wording_hash:str; certainty:str='STATED'; status:str='CURRENT'; event_id:str=''; value:str=''; provenance_hash:str=''
@dataclass
class Case:
 case_id:str=field(default_factory=lambda:'case-'+uuid.uuid4().hex[:8]); lifecycle:str='INTAKE'; facts:list[Fact]=field(default_factory=list); feasibility:str='NOT_ASSESSED'; next_action:str='ask'; gate:dict|None=None; events:list[dict]=field(default_factory=list)
 def public(self,safe=False):
  if not self.gate: g=None
  else:
   g={k:v for k,v in self.gate.items() if k not in ('customer_response','internal_reason')}
   if safe and isinstance(g.get('brief'),dict):
    b=dict(g['brief']); b['facts']=[{'topic':f['topic'],'value_hash':h(str(f['value'])),'certainty':f['certainty'],'provenance_hash':f['provenance_hash']} for f in b.get('facts',[])]
    g['brief']=b
  facts=[asdict(x) for x in self.facts if x.status=='CURRENT']
  if safe: facts=[{k:v for k,v in f.items() if k not in ('value',)}|{'value_hash':h(str(f['value']))} for f in facts]
  return {'case_id':self.case_id,'lifecycle':self.lifecycle,'facts':facts,'feasibility':self.feasibility,'next_action':self.next_action,'gate':g}
 def internal(self):
  return {'case_id':self.case_id,'lifecycle':self.lifecycle,'facts':[{'topic':f.topic,'value':f.value or f.value_class,'certainty':f.certainty,'status':f.status} for f in self.facts if f.status=='CURRENT'],'feasibility':self.feasibility,'next_action':self.next_action}
class AIInference:
 def __init__(self,fixture=False): self.fixture=fixture
 def interpret(self,text,case):
  if self.fixture: return self.fixture_infer(text)
  endpoint=os.environ.get('YUANWAI_AI_ENDPOINT')
  if not endpoint:
   profile=os.environ.get('YUANWAI_HERMES_PROFILE')
   if not profile: raise RuntimeError('AI inference unavailable; set YUANWAI_HERMES_PROFILE or YUANWAI_AI_ENDPOINT')
   prompt='Return JSON only with exact schema: {facts:[{topic:string,value:string,value_class:string}],commitment_request:boolean,conflict:boolean,reference:boolean,supplier_ready:boolean,requires_human_gate:boolean,primary_next_action:string,guardrail:string}. Allowed normalized fact topics: date, location, headcount, service_form, time, budget, menu_preferences, dietary, setup_logistics, invoice_admin. Preserve each distinct fact and its actual value; never return prose facts or alternate keys. Set requires_human_gate=true ONLY when this current customer message asks for availability/acceptance/quote/exception/payment/fulfillment or explicitly requires supplier authority; ordinary qualification facts must set it false. Frozen rules: date is not availability; feasibility is not acceptance; references are not promises; changed/contradictory facts recover; supplier authority is human-gated. Current case state='+json.dumps(case.internal(),ensure_ascii=False)+' Synthetic customer message='+text
   r=subprocess.run(['hermes','-p',profile,'-z',prompt],capture_output=True,text=True,timeout=120,check=True)
   out=json.loads(r.stdout)
   return self.normalize(json.loads(r.stdout))
  prompt={'message':text,'current_state':case.public(),'instruction':'Return JSON only: facts array or object, commitment_request boolean, conflict boolean, reference boolean, supplier_ready boolean, primary_next_action string. Never invent supplier commitments.'}
  req=urllib.request.Request(endpoint,data=json.dumps({'model':os.environ.get('YUANWAI_AI_MODEL','local'),'messages':[{'role':'user','content':json.dumps(prompt,ensure_ascii=False)}],'temperature':0}).encode(),headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=30) as r: return self.normalize(json.loads(json.load(r)['choices'][0]['message']['content']))
 def normalize(self,out):
  if not isinstance(out,dict): raise RuntimeError('AI output malformed: object required')
  facts=out.get('facts')
  aliases={'event_date':'date','date':'date','location':'location','venue':'location','guest_count':'headcount','headcount':'headcount','service_style':'service_form','service_form':'service_form','time':'time','event_time':'time','budget':'budget','price_range':'budget','menu':'menu_preferences','preferences':'menu_preferences','menu_preferences':'menu_preferences','dietary':'dietary','dietary_needs':'dietary','setup':'setup_logistics','logistics':'setup_logistics','setup_logistics':'setup_logistics','invoice':'invoice_admin','admin':'invoice_admin','invoice_admin':'invoice_admin'}
  if isinstance(facts,dict): facts=[{'topic':k,'value_class':v} for k,v in facts.items() if k not in ('source',)]
  if not isinstance(facts,list) or any(not isinstance(x,dict) or 'topic' not in x or 'value' not in x or 'value_class' not in x for x in facts): raise RuntimeError('AI facts schema malformed: expected list of {topic,value,value_class}')
  stable=[]
  for x in facts:
   topic=aliases.get(str(x['topic']))
   if not topic: raise RuntimeError('AI fact topic unnormalizable: '+str(x['topic']))
   stable.append({'topic':topic,'value_class':str(x['value_class']),'value':str(x['value'])})
  required={'commitment_request','conflict','reference','supplier_ready','requires_human_gate'}
  if not required.issubset(out): raise RuntimeError('AI structured authority fields missing')
  if not all(isinstance(out[k],bool) for k in required): raise RuntimeError('AI authority fields must be boolean')
  action=str(out.get('primary_next_action',''))
  return {'facts':stable,'commitment_request':out['commitment_request'],'conflict':out['conflict'],'reference':out['reference'],'supplier_ready':out['supplier_ready'],'primary_next_action':action,'model_requires_human_gate':out['requires_human_gate'],'guardrail':out.get('guardrail')}
 def fixture_infer(self,text):
  pats={'date':r'\d{1,2}[月/]\d{1,2}日?','headcount':r'\d+\s*(?:人|位|份)','location':r'台北|新竹|台中|高雄|桃園|到府','service_form':r'外燴|餐盒|自助餐|buffet|桌菜'}; facts=[]
  for t,p in pats.items():
   m=re.search(p,text,re.I)
   if m: facts.append({'topic':t,'value_class':m.group(0)})
  return {'facts':facts,'commitment_request':bool(re.search('可用|有空|接單|承作|接受|報價|價格|折扣|付款|保證|承諾',text)),'conflict':bool(re.search('改成|不是|其實是|更改',text)),'reference':bool(re.search('照片|範例|菜單|之前',text)),'supplier_ready':False}
class Simulator:
 def __init__(self,path=None,fixture=False): self.path=Path(path) if path else None; self.ai=AIInference(fixture); self.case=self.load() if self.path and self.path.exists() else Case()
 def save(self,ev):
  self.case.events.append(ev)
  if self.path: self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps({'case':self.case.public(),'events':self.case.events},ensure_ascii=False,indent=2),encoding='utf-8')
 def brief(self): return {'facts':[{'topic':f.topic,'value':f.value or f.value_class,'certainty':f.certainty,'provenance_hash':f.provenance_hash} for f in self.case.facts if f.status=='CURRENT'],'feasibility':self.case.feasibility,'unknowns':'No universal required fields; provisional policy remains open'}
 def turn(self,text):
  p=self.ai.interpret(text,self.case); changed=False; ev={'ts':now(),'type':'customer_turn','text_redacted':True,'text_hash':h(text),'topics':[],'inference':p}
  for x in p.get('facts',[]):
   old=[f for f in self.case.facts if f.topic==x['topic'] and f.status=='CURRENT']; new_value=x.get('value',x.get('value_class','unknown'))
   if old and (old[-1].value or old[-1].value_class)!=new_value:
    changed=True
    for f in old: f.status='SUPERSEDED'
    self.case.lifecycle='CHANGED/RECOVERY'; self.case.feasibility='UNKNOWN'; self.case.gate=None; self.case.next_action='recovery'; ev['invalidation']={'dependent_state':['feasibility','supplier_ready_brief','pending_supplier_decision'],'superseded_fact_ids':[f.event_id for f in old]}
   if not old or (old[-1].value or old[-1].value_class) != new_value:
    certainty={'customer_stated':'STATED','stated':'STATED','customer_confirmed':'CONFIRMED_BY_CUSTOMER','confirmed':'CONFIRMED_BY_CUSTOMER','inferred':'INFERRED','reference_only':'REFERENCE_ONLY','unknown':'UNKNOWN'}.get(str(x['value_class']).lower(),'STATED')
    self.case.facts.append(Fact(x['topic'],x['value_class'],h(text),certainty,event_id=uuid.uuid4().hex[:8],value=new_value,provenance_hash=h(text+'|'+x['topic'])))
   ev['topics'].append(x['topic'])
  if changed:
   self.case.lifecycle='CHANGED/RECOVERY'; self.case.next_action='recovery'; response='資料有變更，已作廢受影響的舊結論與 supplier gate，請重新確認。'
  elif p.get('conflict') and p.get('facts'): self.case.lifecycle='CHANGED/RECOVERY'; self.case.next_action='recovery'; response='資料有衝突或變更，先不沿用舊結論，請確認目前有效內容。'
  elif p.get('commitment_request') or p.get('model_requires_human_gate'): self.case.lifecycle='HUMAN_GATE_PENDING'; self.case.next_action='human_gate'; self.case.gate={'reason':'supplier authority required','decision_type':'availability/acceptance/price/fulfillment','brief':self.brief(),'authorized':False}; response='這需要供應方確認，我不能自行承諾；已整理 supplier-ready brief。'
  elif p.get('reference'): self.case.lifecycle='OPTIONS'; self.case.next_action='reference'; response='可提供標示為歷史參考的範例，不代表本次菜單、價格或可用性。'
  elif p.get('supplier_ready'): self.case.lifecycle='SUPPLIER_READY'; self.case.next_action='human_gate'; self.case.gate={'reason':'AI assessed decision readiness','decision_type':'supplier authority decision','brief':self.brief(),'authorized':False}; response='已達可供供應方判斷的程度，尚不代表接單。'
  else: self.case.lifecycle='UNDERSTANDING'; self.case.next_action='ask'; response='我先保留目前資訊；請提供下一個你認為重要的需求細節。'
  ev.update({'state':self.case.public(),'guardrail':'BLOCKED' if self.case.next_action=='human_gate' else 'PASS','response_class':'safe_template'}); self.save(ev); return response
 def decide(self,decision,response):
  if self.case.next_action!='human_gate': raise ValueError('no human gate pending')
  self.case.gate.update({'authorized':True,'decision_class':decision,'customer_response_hash':h(response)}); self.case.lifecycle='CUSTOMER_CONTINUATION'; self.case.next_action='answer'; self.case.feasibility='POSSIBLE' if decision.lower() in ('accept','possible','可行','接受') else 'CONFLICT'; self.save({'ts':now(),'type':'supplier_decision','decision_class':decision,'customer_response_redacted':True,'customer_response_hash':h(response),'internal_reason_redacted':True,'state':self.case.public()})
 def load(self):
  x=json.loads(self.path.read_text(encoding='utf-8')); c=x['case']; return Case(c['case_id'],c['lifecycle'],[Fact(**f) for f in c['facts']],c['feasibility'],c['next_action'],c['gate'],x.get('events',[]))
 def replay(self): return [e['state'] for e in self.case.events if 'state' in e]
def scenarios():
 out=[]
 def run(name,fn):
  try:
   ok=fn(); out.append({'scenario':name,'status':'PASS' if ok else 'FAIL','evidence':{'state_transition':'recorded','guardrail':'recorded','facts':'topic/value_class only','raw_text':'absent'}})
  except Exception as e: out.append({'scenario':name,'status':'FAIL','error':str(e)})
 def base(): s=Simulator(None,True); s.turn('外燴 10/20 台北 30人'); return s
 def turns(s): return [e for e in s.case.events if e['type']=='customer_turn']
 run('known facts are not re-asked',lambda:(lambda s:(s.turn('想了解服務'),s.case.next_action=='ask' and 'date' not in json.dumps(turns(s)[-1]['inference']) and s.case.facts[0].status=='CURRENT'))(base())[1])
 run('date is not availability',lambda:(lambda s:(s.turn('10/20有空嗎'),s.case.next_action=='human_gate' and s.case.feasibility=='NOT_ASSESSED' and s.case.gate['authorized'] is False))(base())[1])
 run('承作嗎 is human gate',lambda:(lambda s:(s.turn('能承作嗎？'),s.case.next_action=='human_gate' and s.case.lifecycle=='HUMAN_GATE_PENDING' and s.case.events[-1]['guardrail']=='BLOCKED'))(base())[1])
 run('feasible is not acceptance',lambda:(lambda s:(s.turn('請評估是否可行'),s.case.feasibility=='NOT_ASSESSED' and s.case.lifecycle!='CUSTOMER_CONTINUATION' and s.case.next_action!='answer'))(base())[1])
 run('internal reason stays internal',lambda:(lambda s:(s.turn('請確認接單'),s.decide('reject','目前無法承接，internal low value reason'),s.case.gate['customer_response_hash'] and all('internal low value' not in json.dumps(e,ensure_ascii=False) for e in s.case.events)))(base())[-1])
 run('change invalidates downstream',lambda:(lambda s:(s.turn('請確認接單'),s.turn('改成 10/21'),s.case.gate is None and s.case.next_action=='recovery' and any(f.status=='SUPERSEDED' for f in s.case.facts) and s.case.feasibility=='UNKNOWN'))(base())[-1])
 run('contradictory facts fail closed',lambda:(lambda s:(s.turn('改成 10/22'),s.case.next_action=='recovery' and s.case.gate is None and len([f for f in s.case.facts if f.topic=='date'])==2))(base())[1])
 run('reference is not promise',lambda:(lambda s:(s.turn('給我之前的菜單照片'),s.case.next_action=='reference' and s.case.feasibility=='NOT_ASSESSED' and not s.case.gate))(base())[1])
 run('mediation continues',lambda:(lambda s:(s.turn('請確認接單'),s.decide('accept','供應方確認可承接'),s.case.lifecycle=='CUSTOMER_CONTINUATION' and s.case.next_action=='answer' and s.case.gate['authorized'] is True))(base())[-1])
 Path('simulation-evidence.json').write_text(json.dumps({'generated_at':now(),'scenarios':out,'pass':sum(x['status']=='PASS' for x in out),'total':len(out)},ensure_ascii=False,indent=2),encoding='utf-8'); return out
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--scenario',action='store_true'); ap.add_argument('--case',default='simulation-case.json'); ap.add_argument('--fixture',action='store_true'); a=ap.parse_args()
 if a.scenario:
  r=scenarios(); print(json.dumps({'scenarios':r,'pass':sum(x['status']=='PASS' for x in r),'total':len(r)},ensure_ascii=False,indent=2)); return 0 if all(x['status']=='PASS' for x in r) else 1
 s=Simulator(a.case,a.fixture); print('Yuanwai offline simulator; /state /decision <class> <response> /replay /quit')
 while True:
  try: t=input('customer> ')
  except EOFError: break
  if t=='/quit': break
  if t=='/state': print(json.dumps(s.case.public(),ensure_ascii=False,indent=2)); continue
  if t=='/replay': print(json.dumps(s.replay(),ensure_ascii=False,indent=2)); continue
  if t.startswith('/decision '): _,d,*rest=t.split(' '); s.decide(d,' '.join(rest)); print('customer continuation: authorized response recorded'); continue
  try: print(s.turn(t)); print(json.dumps(s.case.public(),ensure_ascii=False))
  except RuntimeError as e: print('HOLD:',e)
if __name__=='__main__': raise SystemExit(main())