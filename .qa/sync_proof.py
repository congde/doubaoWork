"""Sync public chapter outlines from the supplied publisher proof (never copy the PDF)."""
import json
import re
import sys
from html import escape
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
pdf = pymupdf.open(sys.argv[1])
def clean(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return re.sub(r'(?<=[\u4e00-\u9fffA-Za-z0-9]) (?=[\u4e00-\u9fff])', '', s)

data = json.loads((ROOT/'guide-data.js').read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
toc = '\n'.join(p.get_text() for p in pdf[6:10])
titles = re.findall(r'第(\d+)\s*章\s+([^\n]+)', toc)
assert len(titles) == 15
for n, title in titles:
    c = data['chapters'][int(n)-1]
    c['title'] = f'第{n}章　{clean(title)}'
    c['short'] = clean(title)
    c['outline'] = []

for pg in list(pdf)[10:]:
    for block in pg.get_text('dict', flags=0)['blocks']:
        lines = block.get('lines', [])
        if not lines:
            continue
        raw = ''.join(''.join(s['text'] for s in line['spans']) for line in lines)
        text = re.sub(r'^(\d+\.\d+(?:\.\d+)?)\s+(.*)$', lambda m: m[1]+' '+clean(m[2]), raw)
        match = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?\s', text)
        if not match or not any(s['color'] == 4677291 for s in lines[0]['spans']):
            continue
        n = int(match[1])
        assert 1 <= n <= 15, text
        c = data['chapters'][n-1]
        if match[3]:
            assert c['outline'][-1]['title'].startswith(f'{n}.{match[2]} '), text
            c['outline'][-1]['children'].append(text)
        else:
            c['outline'].append({'title':text, 'children':[], 'page':pg.number-9})

palette = [('#0071b8','#eef7ff'),('#008577','#eefaf7'),('#9b6200','#fff8eb'),('#7855ae','#f7f2fc'),('#ba516a','#fff3f6')]
def wrap(text, limit):
    # Weight Latin characters at half width, keep Chinese punctuation with its text.
    rows, row, width = [], '', 0
    for char in text:
        w = 1 if ord(char)>255 else .55
        if width+w>limit and char not in '，。；：、）”':
            rows.append(row); row=''; width=0
        row += char; width += w
    if row: rows.append(row)
    return rows

def svg_for(c):
    # A chapter root connects to numbered sections; every leaf is a proof heading.
    parts=[]
    def label(text,x,y,size=25,color='#263c50',weight='400',limit=27):
        rows=wrap(text,limit)
        parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">')
        for i,row in enumerate(rows):
            parts.append(f'<tspan x="{x}" dy="{0 if i==0 else size*1.5}">{escape(row)}</tspan>')
        parts.append('</text>')
        return len(rows)*size*1.5
    title_rows=wrap(c['short'],36)
    top=135+len(title_rows)*52
    heights=[]
    for sec in c['outline']:
        heights.append(72+len(wrap(sec['title'],25))*39+sum(len(wrap(t,29))*34+17 for t in sec['children']))
    positions=[]; y=top+55
    for i in range(0,len(heights),2):
        positions += [(64,y),(930,y)][:len(heights)-i]
        y+=max(heights[i:i+2])+38
    height=max(1050,y+65)
    parts.append(f'<rect width="1800" height="{height}" fill="#fbfcfe"/>')
    label(f'第 {c["n"]:02d} 章 · 结构导图',64,62,23,'#0071b8','600',60)
    label(c['short'],64,122,36,'#143654','700',36)
    label('按小节理解方法，结合正文中的案例与检查项练习。',64,top-12,22,'#63778a','400',65)
    for i,(sec,(x,y)) in enumerate(zip(c['outline'],positions)):
        color,bg=palette[i%5];h=heights[i]
        parts.append(f'<rect x="{x}" y="{y}" width="806" height="{h}" rx="22" fill="{bg}" stroke="{color}" stroke-opacity=".22"/>')
        parts.append(f'<rect x="{x}" y="{y+24}" width="5" height="40" rx="2" fill="{color}"/>')
        used=label(sec['title'],x+30,y+44,26,color,'700',25)
        yy=y+used+64
        if sec['children']:
            parts.append(f'<path d="M {x+34} {yy-16} V {y+h-30}" fill="none" stroke="{color}" stroke-opacity=".3" stroke-width="2"/>')
        for child in sec['children']:
            parts.append(f'<path d="M {x+34} {yy-8} H {x+50}" fill="none" stroke="{color}" stroke-opacity=".4" stroke-width="2"/>')
            yy+=label(child,x+62,yy,23,limit=29)+17
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-label="{escape(c["title"])}结构导图"><style>text{{font-family:Microsoft YaHei,PingFang SC,Noto Sans CJK SC,sans-serif}}</style>'+''.join(parts)+'</svg>'

for c in data['chapters']:
    assert 3 <= len(c['outline']) <= 5, c['n']
    c['spine'] = [s['title'] for s in c['outline']]
    c['summary'] = '本章依次介绍：'+'；'.join(re.sub(r'^\d+\.\d+\s+', '', s['title']) for s in c['outline'])+'。'
    svg_path = f'resources/chapter-mindmaps/ch{c["n"]:02d}.svg'
    c['map'] = c.get('generatedMap', svg_path)
    (ROOT/svg_path).write_text(svg_for(c),encoding='utf-8')
(ROOT/'guide-data.js').write_text('window.BOOK_DATA = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
for path in (ROOT/'resources').rglob('*.html'):
    s=path.read_text(encoding='utf-8')
    t=re.sub(r'(chapter-mindmaps/ch\d{2})\.png',r'\1.svg',s)
    def sync_nodes(value):
        if isinstance(value, dict):
            match = re.fullmatch(r'ch(\d+)', value.get('id', ''))
            if match:
                c = data['chapters'][int(match[1])-1]
                value['title'] = c['title']
                if 'children' in value:
                    value['children'] = {'attached': [
                        {'id':f'proof-{c["n"]}-{i}', 'title':section['title'],
                         'children':{'attached':[
                             {'id':f'proof-{c["n"]}-{i}-{j}', 'title':leaf}
                             for j, leaf in enumerate(section['children'])]}}
                        for i, section in enumerate(c['outline'])]}
                    value['notes'] = {'plain':{'content':c['summary']}}
                return
            for child in value.values(): sync_nodes(child)
        elif isinstance(value, list):
            for child in value: sync_nodes(child)
    def sync_script(match):
        embedded = json.loads(match[2])
        sync_nodes(embedded)
        return match[1]+json.dumps(embedded,ensure_ascii=False)+match[3]
    t = re.sub(r'(<script[^>]*id="(?:data|hub-data|maps)"[^>]*>)(.*?)(</script>)', sync_script, t, flags=re.S)
    if t!=s: path.write_text(t,encoding='utf-8')
print(json.dumps({'chapters':len(data['chapters']),'sections':sum(len(c['outline']) for c in data['chapters']),'subsections':sum(len(s['children']) for c in data['chapters'] for s in c['outline'])},ensure_ascii=False))
