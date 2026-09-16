#!/usr/bin/env python3
"""Move public URLs to ASCII-only paths and rewrite references."""
from pathlib import Path
import json, re, shutil, zipfile

root = Path('/workspace/doubaoWork')

DIR_MOVES = [
    ('resources/skill-kit', 'resources/skill-kit'),
    ('resources/skill-kit/单章下载', 'resources/skill-kit/packs'),
    ('resources/companion', 'resources/companion'),
    ('resources/companion/MindLine原生', 'resources/companion/mindline'),
    ('resources/companion/WPS与通用交换', 'resources/companion/wps'),
    ('resources/overview', 'resources/overview'),
    ('resources/book-map', 'resources/book-map'),
]

FILE_MOVES = [
    ('resources/skill-kit/index.html', 'resources/skill-kit/index.html'),
    ('resources/skill-kit/chapter-maps.html', 'resources/skill-kit/chapter-maps.html'),
    ('resources/skill-kit/book-mindmap.html', 'resources/skill-kit/book-mindmap.html'),
    ('resources/companion/index.html', 'resources/companion/index.html'),
    ('resources/companion/chapter-maps.html', 'resources/companion/chapter-maps.html'),
    ('resources/companion/book-mindmap.html', 'resources/companion/book-mindmap.html'),
    ('resources/companion/使用说明.md', 'resources/companion/README.md'),
    ('resources/overview/打开全面思维导图.html', 'resources/overview/index.html'),
    ('resources/overview/产品功能导图.html', 'resources/overview/features.html'),
    ('resources/overview/操作章节Skill合集.zip', 'resources/overview/skill-collection.zip'),
    ('resources/book-map/打开全书思维导图.html', 'resources/book-map/index.html'),
    ('appendices/book-appendix.pdf', 'appendices/book-appendix.pdf'),
]

ZIP_STEM = {
    1: 'ch01-task-fit.zip',
    2: 'ch02-meeting-minutes.zip',
    3: 'ch03-task-contract.zip',
    4: 'ch04-evidence-report.zip',
    5: 'ch05-presentation-storyboard.zip',
    6: 'ch06-sales-table-audit.zip',
    7: 'ch07-school-evidence-check.zip',
    8: 'ch08-page-register.zip',
    9: 'ch09-monitor-run.zip',
    10: 'ch10-content-brief.zip',
    11: 'ch11-team-action-merge.zip',
    12: 'ch12-weekly-report-check.zip',
    13: 'ch13-permission-review.zip',
    14: 'ch14-role-workflow-card.zip',
    15: 'ch15-pilot-evaluation.zip',
}

TEXT_REPLACES = [
    ('resources/skill-kit/index.html', 'resources/skill-kit/index.html'),
    ('resources/skill-kit/chapter-maps.html', 'resources/skill-kit/chapter-maps.html'),
    ('resources/skill-kit/book-mindmap.html', 'resources/skill-kit/book-mindmap.html'),
    ('resources/skill-kit/packs', 'resources/skill-kit/packs'),
    ('resources/skill-kit', 'resources/skill-kit'),
    ('resources/companion/index.html', 'resources/companion/index.html'),
    ('resources/companion/chapter-maps.html', 'resources/companion/chapter-maps.html'),
    ('resources/companion/book-mindmap.html', 'resources/companion/book-mindmap.html'),
    ('resources/companion/README.md', 'resources/companion/README.md'),
    ('resources/companion/mindline', 'resources/companion/mindline'),
    ('resources/companion/wps', 'resources/companion/wps'),
    ('resources/companion', 'resources/companion'),
    ('resources/overview/index.html', 'resources/overview/index.html'),
    ('resources/overview/features.html', 'resources/overview/features.html'),
    ('resources/overview', 'resources/overview'),
    ('resources/book-map/index.html', 'resources/book-map/index.html'),
    ('resources/book-map', 'resources/book-map'),
    ('appendices/book-appendix.pdf', 'appendices/book-appendix.pdf'),
    ('book-appendix.pdf', 'book-appendix.pdf'),
    ('../skill-kit/packs/', '../skill-kit/packs/'),
    ('packs/all-skills.zip', 'packs/all-skills.zip'),
    ('all-skills.zip', 'all-skills.zip'),
    ('href="packs/"', 'href="packs/"'),
    ("href='packs/'", "href='packs/'"),
    ('href="packs/', 'href="packs/'),
    ("return 'packs/'", "return 'packs/'"),
    ("return '../skill-kit/packs/'", "return '../skill-kit/packs/'"),
    ('href="../index.html"', 'href="../index.html"'),
    ('index.html', 'index.html'),
    ('chapter-maps.html', 'chapter-maps.html'),
    ('book-mindmap.html', 'book-mindmap.html'),
]


def move(src, dst):
    s, d = root / src, root / dst
    if not s.exists():
        print('missing', src)
        return
    d.parent.mkdir(parents=True, exist_ok=True)
    if d.exists():
        print('already', dst)
        return
    shutil.move(str(s), str(d))
    print('moved', src, '->', dst)


for a, b in DIR_MOVES:
    move(a, b)
for a, b in FILE_MOVES:
    move(a, b)

# Rename chapter zips using current Chinese names still in packs/
packs = root / 'resources/skill-kit/packs'
old_zips = sorted(packs.glob('第*.zip'))
html = (root / 'resources/skill-kit/index.html').read_text(encoding='utf-8')
skills = json.loads(re.search(r'<script id="skill-data" type="application/json">(.*?)</script>', html, re.S).group(1))
old_to_new = {}
for s in skills:
    new = ZIP_STEM[s['n']]
    old = s.get('filename')
    old_to_new[old] = new
    src = packs / old
    dst = packs / new
    if src.exists() and src != dst:
        src.rename(dst)
        print('zip', old, '->', new)
    s['filename'] = new

combo_old = packs / 'all-skills.zip'
combo_new = packs / 'all-skills.zip'
# rebuild combined zip with English names
if combo_new.exists():
    combo_new.unlink()
with zipfile.ZipFile(combo_new, 'w') as z:
    for n in range(1, 16):
        p = packs / ZIP_STEM[n]
        z.write(p, p.name)
    readme = packs / 'README.txt'
    # optional
print('wrote', combo_new)
if combo_old.exists() and combo_old != combo_new:
    combo_old.unlink()

# write updated skill-data back into HTML
html = re.sub(
    r'(<script id="skill-data" type="application/json">)(.*?)(</script>)',
    lambda m: m.group(1) + json.dumps(skills, ensure_ascii=False) + m.group(3),
    html,
    count=1,
    flags=re.S,
)
(root / 'resources/skill-kit/index.html').write_text(html, encoding='utf-8')

SKIP_SUFFIX = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.pdf', '.zip', '.woff', '.woff2'}

def rewrite_text(text):
    for a, b in TEXT_REPLACES:
        text = text.replace(a, b)
    for old, new in old_to_new.items():
        text = text.replace(old, new)
    return text

count = 0
for p in root.rglob('*'):
    if not p.is_file():
        continue
    if '.git' in p.parts or p.suffix.lower() in SKIP_SUFFIX:
        continue
    try:
        raw = p.read_text(encoding='utf-8')
    except Exception:
        continue
    new = rewrite_text(raw)
    if new != raw:
        p.write_text(new, encoding='utf-8')
        count += 1
        print('rewrote', p.relative_to(root))
print('rewrote files', count)

# packs listing
items = ['all-skills.zip'] + [ZIP_STEM[n] for n in range(1, 16)]
(packs / 'index.html').write_text('''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Skill packs</title>
  <link rel="stylesheet" href="../../../site.css">
  <style>.wrap{max-width:860px;margin:0 auto;padding:12px 4vw 64px} ul{padding-left:20px;line-height:2}</style>
</head>
<body>
<header class="top">
  <a class="brand" href="../../../index.html">
    <div class="mark" aria-hidden="true">豆</div>
    <div><strong>豆包工作</strong><small>Skill packs</small></div>
  </a>
  <div class="top-actions"><a href="../index.html">Back to skills</a></div>
</header>
<div class="page-intro">
  <div class="eyebrow">Skills</div>
  <h1>Skill packs</h1>
  <p>Each zip has the skill rules, a sample, and a short readme.</p>
</div>
<main class="wrap"><ul>
''' + '\n'.join(f'<li><a href="{name}" download>{name}</a></li>' for name in items) + '''
</ul></main>
</body>
</html>
''', encoding='utf-8')

print('done')
