#!/usr/bin/env python3
"""Public-safe deterministic census for Yuanwai qualification discovery.

Reads a private LINE OA export; emits only aggregate counts and de-identified
sample indices. Raw messages and filenames never appear in output.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, re, zipfile
from collections import Counter
from pathlib import Path

TERMS = {
    "service_type": ["外燴", "外烩", "自助餐", "buffet", "便當", "餐盒", "茶會", "包場", "外帶", "到府", "餐點"],
    "location": ["地址", "地點", "場地", "會場", "哪裡", "哪裏", "台北", "新北", "桃園", "基隆", "新竹", "台中", "台南", "高雄"],
    "date": ["日期", "幾月", "幾號", "幾日", "星期", "週一", "週二", "週三", "週四", "週五", "週六", "週日", "明天", "下週", "月底"],
    "time": ["幾點", "時間", "上午", "下午", "中午", "晚上", "早上", "時段", "點到"],
    "quantity": ["人", "位", "份", "桌", "人數", "幾人", "數量", "幾份"],
    "budget": ["預算", "預計", "預算多少", "一萬", "兩萬", "三萬", "四萬", "費用", "價錢", "價格", "多少錢"],
    "menu": ["菜單", "菜色", "餐點", "葷", "素", "蔬食", "素食", "飲料", "甜點", "口味"],
    "dietary": ["過敏", "不吃", "忌口", "清真", "蛋奶素", "全素", "純素", "無麩質"],
    "equipment_setup": ["設備", "器具", "桌椅", "餐具", "保溫", "加熱", "服務人員", "場佈", "擺盤", "setup"],
    "invoice_admin": ["發票", "統編", "抬頭", "收據", "匯款", "帳戶", "訂金", "押金", "付款"],
    "access_logistics": ["停車", "電梯", "樓梯", "進場", "卸貨", "車位", "交通", "搬運", "路線"],
}
QUESTION_RE = re.compile(r"[?？]|(嗎|呢|可以|請問|想請教|有沒有|能否|是否|幾|多少|哪裡|哪裏)")
PRICE_RE = re.compile(r"(\$|NT|元|費用|價格|價錢|報價|預算|一萬|兩萬|三萬|四萬|五萬|六萬|七萬|八萬|九萬|十萬)")


def hit(text, terms):
    return any(t.lower() in text.lower() for t in terms)


def load(path):
    files = []
    total = 0
    with zipfile.ZipFile(path) as z:
        names = sorted(n for n in z.namelist() if n.lower().endswith('.csv'))
        for idx, name in enumerate(names, 1):
            rows = list(csv.DictReader(io.StringIO('\n'.join(z.read(name).decode('utf-8-sig', errors='replace').split('\n')[3:]))))
            rows = [r for r in rows if any((v or '').strip() for v in r.values())]
            total += len(rows)
            files.append((idx, rows))
    return files, total


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('zipfile'); ap.add_argument('--out', required=True)
    a = ap.parse_args(); p = Path(a.zipfile)
    sha = hashlib.sha256(p.read_bytes()).hexdigest().upper()
    files, total = load(p)
    census = Counter(); first = Counter(); stages = Counter(); q = Counter(); price_paths = []
    service = Counter(); sampled = []
    for idx, rows in files:
        texts = [(r.get('內容') or '').replace('\r',' ').replace('\n',' ') for r in rows]
        senders = [(r.get('傳送者類型') or '') for r in rows]
        customer = [t for t,s in zip(texts,senders) if 'User' in s or '使用者' in s or 'Customer' in s]
        if not customer: customer = texts
        for field, terms in TERMS.items():
            if any(hit(t, terms) for t in customer): census[field] += 1
        for field, terms in TERMS.items():
            if customer and hit(customer[0], terms): first[field] += 1
        for t,s in zip(texts,senders):
            if QUESTION_RE.search(t) and ('Account' in s or '官方' in s or '樹朵' in s): q['supplier_question_messages'] += 1
        pi = next((i for i,t in enumerate(texts) if PRICE_RE.search(t) and ('Account' in senders[i] or '官方' in senders[i] or '樹朵' in senders[i])), None)
        if pi is not None: price_paths.append(pi+1)
        if any(hit(t, TERMS['service_type']) for t in customer): service['service_type_present'] += 1
        if idx in {1, 75, 150, 225, 300, 375}: sampled.append({'case_index':idx,'message_count':len(rows),'first_customer_has': [f for f,terms in TERMS.items() if customer and hit(customer[0],terms)]})
    out = {'schema_version':'0.1','corpus':{'sha256':sha,'csv_files':len(files),'messages_after_metadata_header':total},'method':{'kind':'deterministic_lexical_census','raw_output':'never emitted','case_sample_indices':[x['case_index'] for x in sampled]},'counts':{'case_level_any_observed':dict(census),'first_customer_message_observed':dict(first),'supplier_questions':dict(q),'supplier_price_signal_message_position':{'n':len(price_paths),'median':sorted(price_paths)[len(price_paths)//2] if price_paths else None}},'sample_readback':sampled}
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__': main()
