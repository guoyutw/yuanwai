#!/usr/bin/env python3
"""Bounded, public-safe Issue #70 remediation census.

The input ZIP remains private. Output contains aggregates and case indices only.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,zipfile
from collections import Counter,defaultdict
from pathlib import Path
FIELDS={
 'service_type':['外燴','外烩','自助餐','buffet','便當','餐盒','茶會','包場','外帶','到府'],
 'location':['地址','地點','場地','會場','哪裡','哪裏','台北','新北','桃園','基隆','新竹','台中','台南','高雄'],
 'date':['日期','幾月','幾號','幾日','星期','週一','週二','週三','週四','週五','週六','週日','明天','下週','月底'],
 'time':['幾點','時間','上午','下午','中午','晚上','早上','時段'],
 'quantity':['人','位','份','桌','人數','幾人','數量','幾份'],
 'budget':['預算','費用','價格','價錢','多少錢','元','萬'],
 'menu':['菜單','菜色','餐點','葷','素','蔬食','飲料','甜點','口味'],
 'dietary':['過敏','不吃','忌口','清真','蛋奶素','全素','純素'],
 'equipment_setup':['設備','器具','桌椅','餐具','保溫','加熱','服務人員','場佈','擺盤'],
 'access_logistics':['停車','電梯','樓梯','進場','卸貨','車位','交通','搬運'],
 'invoice_admin':['發票','統編','抬頭','收據','匯款','帳戶','訂金','押金','付款'],
}
Q=re.compile(r'[?？]|(嗎|呢|可以|請問|想請教|有沒有|能否|是否|幾|多少|哪裡|哪裏)')
# Strict enough to exclude a bare budget question: supplier message must contain
# a numeric/unit or an explicit quote/proposal phrase.
STRICT_PRICE=re.compile(r'(報價單|報價|方案.*(元|萬)|\d[\d,]*(?:\.?\d+)?\s*(?:元|萬)|(?:一|二|三|四|五|六|七|八|九|十)萬)')

def hit(s,terms): return any(t.lower() in s.lower() for t in terms)
def load(p):
 with zipfile.ZipFile(p) as z:
  out=[]
  for i,n in enumerate(sorted(x for x in z.namelist() if x.lower().endswith('.csv')),1):
   rows=[r for r in csv.DictReader(io.StringIO('\n'.join(z.read(n).decode('utf-8-sig','replace').splitlines()[3:]))) if any((v or '').strip() for v in r.values())]
   out.append((i,rows))
 return out

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('zipfile'); ap.add_argument('--out',required=True); a=ap.parse_args(); p=Path(a.zipfile)
 cases=load(p); reask=Counter(); field_price=defaultdict(Counter); service=Counter(); sample=[]; price_positions=[]
 for idx,rows in cases:
  msgs=[(r.get('傳送者類型',''),(r.get('內容') or '').replace('\n',' ')) for r in rows]
  user_seen=set(); first_price=None; first_service='other'
  if any(hit(t,FIELDS['service_type']) for s,t in msgs[:4] if s=='User'): first_service='service_signal'
  for j,(sender,text) in enumerate(msgs):
   if sender=='Account':
    for f,terms in FIELDS.items():
     if hit(text,terms) and Q.search(text) and f not in {x for x in user_seen if x}:
      reask[f]+=1
    if first_price is None and STRICT_PRICE.search(text): first_price=j+1
   elif sender=='User':
    for f,terms in FIELDS.items():
     if hit(text,terms): user_seen.add(f)
  if first_price: price_positions.append(first_price)
  # Event-based field timing: field first appears in User messages before/after strict price.
  if first_price:
   for f,terms in FIELDS.items():
    pos=next((j+1 for j,(s,t) in enumerate(msgs) if s=='User' and hit(t,terms)),None)
    if pos is not None: field_price[f]['pre' if pos<=first_price else 'post']+=1
  if idx in {1,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375}: sample.append({'case_index':idx,'message_count':len(rows),'service_bucket':first_service})
 out={'schema_version':'0.2-remediation','corpus':{'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper(),'csv_files':len(cases),'messages':sum(len(r) for _,r in cases)},'method':{'supplier_followup_proxy':'Account message contains field term + question marker, after checking prior User mentions; proxy is not causal ground truth','strict_price_event':'first Account message matching explicit quote/proposal or numeric currency/unit expression','raw_output':'never emitted'},'q3_field_followup_proxy_counts':dict(reask),'q5_strict_price_event':{'cases':len(price_positions),'message_position_median':sorted(price_positions)[len(price_positions)//2] if price_positions else None,'field_user_presence_relative_to_event':{f:dict(v) for f,v in field_price.items()}},'bounded_validation_sample':sample}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
