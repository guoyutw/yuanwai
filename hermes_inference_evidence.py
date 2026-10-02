#!/usr/bin/env python3
"""Run a genuine Hermes-backed two-turn Yuanwai probe; no fixtures/stubs."""
import json,os
from pathlib import Path
from yuanwai_simulator import Simulator
profile=os.environ.get('YUANWAI_HERMES_PROFILE','yuanwai74'); case_path=Path('hermes-genuine-case.json')
if case_path.exists(): case_path.unlink()
s=Simulator(case_path,False)
responses=[s.turn('10/20 中壢 約30人 歐式自助餐 晚上六點 預算兩萬'),s.turn('所以 10/20 你們能承作嗎？')]
gate_snapshot=s.case.public(safe=True)['gate']
responses.append(s.turn('改成 10/21')); responses.append(s.turn('日期是 10/21')); responses.append(s.turn('所以 10/21 你們能承作嗎？'))
try: s.decide('accept','供應方內部確認檔期與人力','我們確認 10/21 可以承作，接下來會與您確認細節。')
except ValueError as e: raise AssertionError(e)
assert s.case.lifecycle=='CUSTOMER_CONTINUATION' and s.case.gate['authorized_customer_response'].startswith('我們確認')
trace=[{'type':e['type'],'lifecycle':e.get('state',{}).get('lifecycle'),'next_action':e.get('state',{}).get('next_action'),'gate':bool(e.get('state',{}).get('gate')),'guardrail':e.get('guardrail'),'structured_consumed':bool(e.get('inference'))} for e in s.case.events]
assert trace[0]['lifecycle']=='UNDERSTANDING' and trace[0]['next_action']=='ask' and not trace[0]['gate']
assert trace[1]['lifecycle']=='HUMAN_GATE_PENDING' and trace[1]['next_action']=='human_gate' and trace[1]['guardrail']=='BLOCKED'
assert trace[2]['lifecycle']=='CHANGED/RECOVERY' and not trace[2]['gate'] and trace[2]['next_action']=='recovery'
vals=[(f.topic,f.value) for f in s.case.facts]; assert ('date','10/20') in vals and ('date','10/21') in vals
assert len([f for f in s.case.facts if f.topic=='date' and f.status=='CURRENT'])==1
gate_brief=gate_snapshot
evidence={'fixture':False,'backend':'Hermes CLI genuine inference','profile_class':'isolated dev/test profile','profile':profile,'inference_turns':5,'structured_result_consumed':all(x['structured_consumed'] for x in trace),'trace':trace,'gate_brief_public':gate_brief,'decision_continuation':{'decision_class':'accept','internal_reason_redacted':True,'authorized_response_hash':__import__('yuanwai_simulator').h(s.case.gate['authorized_customer_response']),'lifecycle':s.case.lifecycle,'outward_response_redacted':True},'final_next_action':s.case.next_action,'provider_model_product_decision':False,'raw_customer_text_persisted':False}
Path('genuine-hermes-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(evidence,ensure_ascii=False,indent=2))
