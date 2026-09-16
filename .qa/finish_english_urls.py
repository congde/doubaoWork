#!/usr/bin/env python3
"""Rename leftover Chinese public files and English-ize download names."""
from pathlib import Path
from urllib.parse import quote
import io, json, re, zipfile

root = Path('/workspace/doubaoWork')

CHAPTER_MM = {
    '全书思维导图': 'book',
    '第1章_认识豆包工作': 'ch01',
    '第2章_快速上手': 'ch02',
    '第3章_核心概念': 'ch03',
    '第4章_文档写作': 'ch04',
    '第5章_PPT制作': 'ch05',
    '第6章_表格与数据分析': 'ch06',
    '第7章_深度调研与专业分析': 'ch07',
    '第8章_操作电脑与浏览器': 'ch08',
    '第9章_定时任务与流程自动化': 'ch09',
    '第10章_创意内容生成': 'ch10',
    '第11章_连接飞书': 'ch11',
    '第12章_生态扩展': 'ch12',
    '第13章_安全与隐私': 'ch13',
    '第14章_岗位与业务场景': 'ch14',
    '第15章_未来展望': 'ch15',
}

FILE_MOVES = [
    ('resources/skill-kit/先看这里.txt', 'resources/skill-kit/README.txt'),
    ('resources/overview/先看这里.txt', 'resources/overview/README.txt'),
    ('resources/overview/全面思维导图_总览.png', 'resources/overview/overview.png'),
    ('resources/overview/功能详解与资料依据.md', 'resources/overview/feature-sources.md'),
    ('resources/overview/功能详解结构.json', 'resources/overview/features.json'),
    ('resources/overview/完整结构.json', 'resources/overview/structure.json'),
    ('resources/overview/导图说明与来源.md', 'resources/overview/sources.md'),
    ('resources/overview/豆包工作全面导图.drawio', 'resources/overview/overview.drawio'),
    ('resources/overview/豆包工作全面导图.mm', 'resources/overview/overview.mm'),
    ('resources/overview/豆包工作全面导图.xmind', 'resources/overview/overview.xmind'),
    ('resources/overview/豆包工作功能详解.mm', 'resources/overview/features.mm'),
    ('resources/overview/豆包工作功能详解.xmind', 'resources/overview/features.xmind'),
    ('resources/book-map/使用说明.txt', 'resources/book-map/README.txt'),
    ('resources/book-map/完整结构.json', 'resources/book-map/structure.json'),
    ('resources/book-map/豆包工作_全书完整导图.mm', 'resources/book-map/book-map.mm'),
    ('resources/book-map/豆包工作_全书完整导图.xmind', 'resources/book-map/book-map.xmind'),
]


def move(src, dst):
    s, d = root / src, root / dst
    if not s.exists():
        print('missing', src)
        return
    if d.exists():
        print('already', dst)
        return
    s.rename(d)
    print('moved', src, '->', dst)


for a, b in FILE_MOVES:
    move(a, b)

for folder, ext in [('companion/mindline', '.mm'), ('companion/wps', '.xmind')]:
    d = root / 'resources' / folder
    for stem, new in CHAPTER_MM.items():
        move(f'resources/{folder}/{stem}{ext}', f'resources/{folder}/{new}{ext}')

# Rebuild skill zips with English internal names
ZIP_INNER = {
    '先看这里.txt': 'README.txt',
    '示例_复制即用.txt': 'sample.txt',
    '我的任务_替换材料.txt': 'my-task.txt',
}
packs = root / 'resources/skill-kit/packs'
for zpath in sorted(packs.glob('ch*.zip')):
    with zipfile.ZipFile(zpath, 'r') as zin:
        names = zin.namelist()
        if not any(n.split('/')[-1] in ZIP_INNER for n in names):
            continue
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                parts = info.filename.split('/')
                parts[-1] = ZIP_INNER.get(parts[-1], parts[-1])
                new_name = '/'.join(parts)
                zout.writestr(new_name, data)
    zpath.write_bytes(buf.getvalue())
    print('repacked', zpath.name)

combo = packs / 'all-skills.zip'
if combo.exists():
    combo.unlink()
with zipfile.ZipFile(combo, 'w') as z:
    for p in sorted(packs.glob('ch*.zip')):
        z.write(p, p.name)
print('wrote', combo)

TEXT_REPLACES = [
    ('已发起下载；解压后打开 README.txt。', '已发起下载；解压后打开 README.txt。'),
    ("a.download='overview.'+ext", "a.download='overview.'+ext"),
    ("download(D.featurefiles[ext],'features.'+ext)", "download(D.featurefiles[ext],'features.'+ext)"),
    ("download(D.allzip,'skill-collection.zip')", "download(D.allzip,'skill-collection.zip')"),
    ("download(c[ext],'ch'+String(c.skill.n).padStart(2,'0')+'-mindmap.'+ext)", "download(c[ext],'ch'+String(c.skill.n).padStart(2,'0')+'-mindmap.'+ext)"),
    ("el('download').download=m.title.replace(/[\\/:*?\"<>|]/g,'_')+'.png'", "el('download').download=(m.src.split('/').pop()||(m.id+'.png'))"),
    ('请打开 <a href="packs/">skill packs</a>', '请打开 <a href="packs/">skill packs</a>'),
    ('请打开 <a href="../skill-kit/packs/">skill packs</a>', '请打开 <a href="../skill-kit/packs/">skill packs</a>'),
    ('优先打开 `mindline/` 中的 16 个 `.mm` 文件', '优先打开 `mindline/` 中的 16 个 `.mm` 文件'),
    ('使用 `wps/` 中的 16 个 `.xmind` 文件', '使用 `wps/` 中的 16 个 `.xmind` 文件'),
]


def rewrite(path: Path):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return False
    new = text
    for a, b in TEXT_REPLACES:
        new = new.replace(a, b)
    if new != text:
        path.write_text(new, encoding='utf-8')
        print('rewrote', path.relative_to(root))
        return True
    return False


count = 0
for p in root.rglob('*'):
    if not p.is_file() or '.git' in p.parts:
        continue
    if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.pdf', '.zip', '.woff', '.woff2', '.mm', '.xmind', '.drawio'}:
        continue
    if rewrite(p):
        count += 1
print('rewrote files', count)

# Confirm skill JSON filenames stay English
html = (root / 'resources/skill-kit/index.html').read_text(encoding='utf-8')
skills = json.loads(re.search(r'<script id="skill-data" type="application/json">(.*?)</script>', html, re.S).group(1))
print('filenames', [s['filename'] for s in skills])

# Print encoded nginx hints
legacy = [
    'resources/章节技能_即用版/打开这里.html',
    'resources/思维导图与章节技能/打开这里.html',
    'resources/豆包工作全面思维导图/打开全面思维导图.html',
    'resources/豆包Word整体思维导图/打开全书思维导图.html',
    'appendices/附录-20条指令模版+20个常见问题解答+24个核心术语速查.pdf',
]
for p in legacy:
    print('ENC', quote(p, safe='/'))
print('done')
