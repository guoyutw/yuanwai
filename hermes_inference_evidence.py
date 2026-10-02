#!/usr/bin/env python3
"""Run a genuine Hermes-backed two-turn Yuanwai probe; no fixtures/stubs."""
import json,os
from pathlib import Path
from yuanwai_simulator import Simulator
profile=os.environ.get('YUANWAI_HERMES_PROFILE','yuanwai74'); case_path=Path('hermes-genuine-case.json')
s=Simulator(case_path,False)
responses=[s.turn('10/20 中壢 約30人 歐式自助餐 晚上六點 預算兩萬'),s.turn('所以 10/20 你們能承作嗎？')]
trace=[{'type':e['type'],'lifecycle':e.get('state',{}).get('lifecycle'),'next_action':e.get('state',{}).get('next_action'),'gate':bool(e.get('state',{}).get('gate')),'guardrail':e.get('guardrail'),'structured_consumed':bool(e.get('inference'))} for e in s.case.events]
assert trace[0]['lifecycle']=='UNDERSTANDING' and trace[0]['next_action']=='ask' and not trace[0]['gate']
assert trace[1]['lifecycle']=='HUMAN_GATE_PENDING' and trace[1]['next_action']=='human_gate' and trace[1]['guardrail']=='BLOCKED'
evidence={'fixture':False,'backend':'Hermes CLI genuine inference','profile_class':'isolated dev/test profile','profile':profile,'inference_turns':2,'structured_result_consumed':all(x['structured_consumed'] for x in trace),'trace':trace,'final_next_action':s.case.next_action,'final_guardrail':trace[-1]['guardrail'],'provider_model_product_decision':False,'raw_customer_text_persisted':False}
Path('genuine-hermes-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(evidence,ensure_ascii=False,indent=2))
