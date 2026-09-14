from pathlib import Path
import json, re
from PIL import Image

root = Path(__file__).resolve().parents[1]
data = json.loads(re.sub(r';\s*$', '', re.sub(r'^window.BOOK_DATA\s*=\s*', '', (root/'guide-data.js').read_text(encoding='utf-8'))))
checked = 0
for c in data['chapters']:
    p = root / c['map']
    assert p.exists(), p
    with Image.open(p) as im:
        assert im.width >= 1536 and im.height >= 1024, (p, im.size)
        im.verify()
    checked += 1
refs = 0
for p in (root/'resources').rglob('*.html'):
    s = p.read_text(encoding='utf-8')
    for ident in ['skill-data', 'maps', 'hub-data']:
        match = re.search(r'<script id="'+ident+r'"[^>]*>(.*?)</script>', s, re.S)
        if not match:
            continue
        d = json.loads(match[1])
        if ident == 'skill-data':
            paths = [c['preview'] for c in d]
        elif ident == 'maps':
            paths = [c['src'] for c in d if c['id'].startswith('ch')]
        else:
            paths = [c['skill']['preview'] for c in d['chapters']]
        assert len(paths) == 15, (p, len(paths))
        for path in paths:
            assert 'chapter-mindmaps' in path, (p,path)
            assert (p.parent/path).exists(), (p,path)
            refs += 1
        if ident == 'skill-data':
            assert '章节导图预览.html' in s
            assert (p.parent/'章节导图预览.html').exists()
print(json.dumps({'chapter_images':checked,'updated_embedded_references':refs,'result':'passed'},ensure_ascii=False))
