#!/usr/bin/env python3
"""Restyle remaining HTML pages to match index.html (light gray + blue chrome)."""
from pathlib import Path
import re

root = Path('/workspace/doubaoWork')

CHROME = '''<header class="top">
  <a class="brand" href="{home}">
    <div class="mark" aria-hidden="true">豆</div>
    <div><strong>豆包工作</strong><small>{subtitle}</small></div>
  </a>
  <div class="top-actions">{actions}</div>
</header>'''

COLOR_MAP = [
    ('#163e36', 'var(--text)'),
    ('#1e483b', 'var(--text)'),
    ('#205342', 'var(--accent)'),
    ('#285943', 'var(--accent)'),
    ('#174e41', 'var(--accent-hover)'),
    ('#1d6553', 'var(--accent)'),
    ('#254c43', 'var(--text)'),
    ('#24483d', 'var(--text)'),
    ('#204d3a', 'var(--text)'),
    ('#275542', 'var(--text)'),
    ('#236f56', 'var(--accent)'),
    ('#2d7054', 'var(--accent)'),
    ('#356049', 'var(--accent)'),
    ('#235e48', 'var(--accent)'),
    ('#39624f', 'var(--accent)'),
    ('#54856e', '#afcae5'),
    ('#164f3b', 'var(--text)'),
    ('#287356', 'var(--accent)'),
    ('#f4f6f3', 'var(--bg)'),
    ('#f2f5f2', 'var(--bg)'),
    ('#eff3ef', 'var(--bg)'),
    ('#f3f6f2', 'var(--bg)'),
    ('#f7f9f6', 'var(--bg)'),
    ('#fbfcfa', '#fff'),
    ('#f6f8f3', 'var(--bg)'),
    ('#f5f7f3', '#f4f8fc'),
    ('#e4f1e9', 'var(--soft)'),
    ('#d9eade', 'var(--soft)'),
    ('#e6eee3', 'var(--soft)'),
    ('#e7eee5', 'var(--soft)'),
    ('#e9efe4', 'var(--soft)'),
    ('#eaf1e5', 'var(--soft)'),
    ('#e9f2ea', 'var(--soft)'),
    ('#edf4ef', 'var(--soft)'),
    ('#eef3ef', '#f4f8fc'),
    ('#dfe6df', 'var(--line)'),
    ('#d4e0d6', 'var(--line)'),
    ('#ceddd0', 'var(--line)'),
    ('#ceddce', 'var(--line)'),
    ('#b4c9bd', 'var(--line)'),
    ('#b7cdbf', 'var(--line)'),
    ('#adc7b7', 'var(--line)'),
    ('#acc5b4', 'var(--line)'),
    ('#b4cbb8', 'var(--line)'),
    ('#b4cbb7', 'var(--line)'),
    ('#bdccbd', 'var(--line)'),
    ('#bdcebf', 'var(--line)'),
    ('#b9ccb9', 'var(--line)'),
    ('#b9cdbd', 'var(--line)'),
    ('#b9cbc2', 'var(--line)'),
    ('#c6d5cf', 'var(--line)'),
    ('#cddbcf', 'var(--line)'),
    ('#d0ded1', 'var(--line)'),
    ('#d2ded1', 'var(--line)'),
    ('#d4dfd0', 'var(--line)'),
    ('#d4dfd5', 'var(--line)'),
    ('#d5dfd2', 'var(--line)'),
    ('#d6e0d3', 'var(--line)'),
    ('#d6e0d5', 'var(--line)'),
    ('#d8e1d5', 'var(--line)'),
    ('#dfe7df', 'var(--line)'),
    ('#e0e8e1', 'var(--line)'),
    ('#e8ede4', 'var(--line)'),
    ('#cee0d7', 'var(--muted)'),
    ('#d0e4d9', 'var(--muted)'),
    ('#d2e0d8', 'var(--muted)'),
    ('#d1e3d8', 'var(--muted)'),
    ('#637c6e', 'var(--muted)'),
    ('#60766c', 'var(--muted)'),
    ('#63776d', 'var(--muted)'),
    ('#6c8075', 'var(--muted)'),
    ('#6e7b64', 'var(--muted)'),
    ('#65836b', 'var(--accent)'),
    ('#476c4e', 'var(--accent)'),
    ('#8faf94', '#91b8ea'),
    ('#dfbd80', 'var(--accent)'),
    ('#c89639', '#0088ee80'),
    ('#e6ae4d', '#0088ee80'),
    ('#f4efe2', '#f4f8fc'),
    ('#132f2866', '#17223640'),
    ('#214c3b12', '#345b8010'),
    ('#17392a0a', '#19385808'),
]

def restyle_css(css: str) -> str:
    out = css
    for old, new in COLOR_MAP:
        out = re.sub(re.escape(old), new, out, flags=re.I)
        out = re.sub(re.escape(old.upper()), new, out)
    out = re.sub(r'font:\s*\d+px/[\d.]+ "Microsoft YaHei",sans-serif',
                 'font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei","PingFang SC",sans-serif',
                 out)
    return out

def inject_link(html: str, href: str) -> str:
    if 'href="' + href + '"' in html or "href='" + href + "'" in html:
        return html
    if '<link rel="stylesheet" href="' + href + '">' in html:
        return html
    html = re.sub(r'(<head[^>]*>)', r'\1<link rel="stylesheet" href="' + href + '">', html, count=1, flags=re.I)
    return html

def restyle_style_tags(html: str) -> str:
    def repl(m):
        return m.group(1) + restyle_css(m.group(2)) + m.group(3)
    return re.sub(r'(<style[^>]*>)(.*?)(</style>)', repl, html, flags=re.S | re.I)

def replace_header(html, home, subtitle, extra_actions='', intro=None):
    actions = extra_actions or f'<a href="{home}">返回阅读指南</a>'
    chrome = CHROME.format(home=home, subtitle=subtitle, actions=actions)
    if intro:
        chrome += intro
    new, n = re.subn(r'<header\b[^>]*>.*?</header>', chrome, html, count=1, flags=re.S | re.I)
    if n:
        return new
    return html.replace('<body>', '<body>' + chrome, 1)

# --- appendices ---
appendix_style = '''
.wrap{max-width:860px;margin:28px auto 64px;padding:28px 24px 40px;background:var(--panel);border:1px solid var(--line);border-radius:20px}
.wrap > h1:first-child{color:var(--text);font-size:28px;letter-spacing:-.4px}
.wrap h2{color:var(--text);margin-top:1.6em}
.wrap h3{color:var(--accent)}
.wrap a{color:var(--accent)}
.wrap blockquote{margin:12px 0;padding:10px 16px;background:#f4f8fc;border-left:4px solid var(--accent);color:#394554}
.wrap table{border-collapse:collapse;width:100%;margin:16px 0;font-size:14px;overflow-x:auto;display:block}
.wrap th,.wrap td{border:1px solid var(--line);padding:8px 10px;vertical-align:top}
.wrap th{background:var(--soft);text-align:left}
.wrap img{max-width:100%;height:auto;display:block;margin:12px 0}
.wrap code{background:#f4f8fc;padding:1px 5px;border-radius:4px}
.wrap hr{border:0;border-top:1px solid var(--line);margin:28px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:17px;padding:21px;margin-bottom:14px}
.card h2{margin:0 0 8px;font-size:20px}
.card p{margin:0 0 12px;color:var(--muted)}
'''

def write_appendix(path: Path, title: str, subtitle: str, inner_after_header: str):
    home = '../index.html'
    html = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="../site.css">
  <style>{appendix_style}</style>
</head>
<body>
{CHROME.format(home=home, subtitle=subtitle, actions=f'<a href="{home}">返回阅读指南</a><a href="./">附录目录</a>')}
<div class="page-intro">
  <div class="eyebrow">书籍附录</div>
  <h1>{title.split("·")[0].strip()}</h1>
</div>
{inner_after_header}
</body>
</html>
'''
    path.write_text(html, encoding='utf-8')
    print('wrote', path)

# Keep appendix body content
for name, title in [
    ('appendix-a.html', '附录A：常用指令模板20条 · 豆包工作'),
    ('appendix-b.html', '附录B：常见问题与排查20问 · 豆包工作'),
    ('appendix-c.html', '附录C：学习资源与持续实践 · 豆包工作'),
]:
    p = root / 'appendices' / name
    raw = p.read_text(encoding='utf-8')
    m = re.search(r'<main class="wrap">(.*)</main>', raw, re.S)
    inner = '<main class="wrap">' + (m.group(1) if m else '') + '</main>'
    write_appendix(p, title, '书籍附录', inner)

# appendix index
idx = root / 'appendices' / 'index.html'
idx.write_text(f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>书籍附录 · 豆包工作</title>
  <link rel="stylesheet" href="../site.css">
  <style>{appendix_style}</style>
</head>
<body>
{CHROME.format(home='../index.html', subtitle='书籍附录', actions='<a href="../index.html">返回阅读指南</a>')}
<div class="page-intro">
  <div class="eyebrow">书籍附录</div>
  <h1>书籍附录</h1>
  <p>三个附录可直接在线阅读。也可下载完整 PDF：20 条指令模板、20 个常见问题解答、24 个核心术语速查。</p>
</div>
<main class="wrap" style="background:transparent;border:0;padding:0 4vw 48px;max-width:860px">
  <article class="card">
    <h2>完整附录 PDF</h2>
    <p>一份文件收录附录 A、B、C 中最常用的三部分，可在线预览或下载后离线查阅。</p>
    <a class="btn" href="book-appendix.pdf?v=20260914" download="book-appendix.pdf">下载附录 PDF</a>
  </article>
  <article class="card">
    <h2>附录 A：常用指令模板 20 条</h2>
    <p>按办公场景选择模板，替换占位符后使用。使用前补齐数据来源、输出格式、操作边界和验收标准。</p>
    <a class="btn ghost" href="appendix-a.html">阅读附录 A</a>
  </article>
  <article class="card">
    <h2>附录 B：常见问题与排查 20 问</h2>
    <p>按主题定位问题。版本性信息需结合当前官方说明复核。</p>
    <a class="btn ghost" href="appendix-b.html">阅读附录 B</a>
  </article>
  <article class="card">
    <h2>附录 C：学习资源与持续实践</h2>
    <p>配套资源入口、14 天实践路线、核心术语速查和全书导图。</p>
    <a class="btn ghost" href="appendix-c.html">阅读附录 C</a>
  </article>
</main>
</body>
</html>
''', encoding='utf-8')
print('wrote', idx)

# zip listing
listing = root / 'resources/skill-kit/packs/index.html'
zips = sorted([p.name for p in listing.parent.iterdir() if p.suffix == '.zip'])
items = '\n'.join(f'<li><a href="{name}" download>{name}</a></li>' for name in zips)
listing.write_text(f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>技能文件包</title>
  <link rel="stylesheet" href="../../../site.css">
  <style>.wrap{{max-width:860px;margin:0 auto;padding:12px 4vw 64px}} ul{{padding-left:20px;line-height:2}}</style>
</head>
<body>
{CHROME.format(home='../../../index.html', subtitle='技能文件包', actions='<a href="../index.html">返回随书技能</a>')}
<div class="page-intro">
  <div class="eyebrow">随书技能</div>
  <h1>技能文件包</h1>
  <p>每个压缩包含技能规则、示例和“先看这里.txt”。解压后即可复制试用。</p>
</div>
<main class="wrap"><ul>
{items}
</ul></main>
</body>
</html>
''', encoding='utf-8')
print('wrote', listing)

# Resource HTML pages: restyle CSS + chrome header
pages = [
    (root / 'resources/skill-kit/chapter-maps.html', '../../index.html', '章节导图', '思维导图'),
    (root / 'resources/companion/chapter-maps.html', '../../index.html', '章节导图', '思维导图'),
    (root / 'resources/skill-kit/book-mindmap.html', '../../index.html', '全书思维导图', '思维导图'),
    (root / 'resources/companion/book-mindmap.html', '../../index.html', '全书思维导图', '思维导图'),
    (root / 'resources/book-map/index.html', '../../index.html', '全书思维导图', '思维导图'),
    (root / 'resources/overview/index.html', '../../index.html', '全面思维导图', '学习与实践全景'),
    (root / 'resources/overview/features.html', '../../index.html', '产品功能', '产品功能导图'),
]

EXTRA_CSS = '''
header.top{background:#ffffffdb!important;color:var(--text)!important;padding:12px max(4vw,24px)!important;min-height:76px!important;border-bottom:1px solid #dedee580!important}
header.top h1,header.top>p{display:none}
nav{top:76px!important}
nav a[aria-current=true],button.active,button.primary{background:var(--accent)!important;color:#fff!important;border-color:var(--accent)!important}
.node.root{background:var(--accent)!important;color:#fff!important;border-color:var(--accent)!important}
'''

for path, home, subtitle, intro_label in pages:
    html = path.read_text(encoding='utf-8')
    # capture original header text
    hm = re.search(r'<header\b[^>]*>(.*?)</header>', html, re.S | re.I)
    h1 = '配套页面'
    lead = ''
    if hm:
        t = re.search(r'<h1[^>]*>(.*?)</h1>', hm.group(1), re.S | re.I)
        p = re.search(r'<p[^>]*>(.*?)</p>', hm.group(1), re.S | re.I)
        if t:
            h1 = re.sub(r'<[^>]+>', '', t.group(1)).strip()
        if p:
            lead = re.sub(r'<[^>]+>', '', p.group(1)).strip()
    html = inject_link(html, home.replace('index.html', 'site.css'))
    html = restyle_style_tags(html)
    intro = f'<div class="page-intro"><div class="eyebrow">{intro_label}</div><h1>{h1}</h1>'
    if lead:
        intro += f'<p>{lead}</p>'
    intro += '</div>'
    html = replace_header(html, home, subtitle, intro=intro)
    # append a small override style
    if 'site-theme-override' not in html:
        html = html.replace('</head>', '<style id="site-theme-override">' + EXTRA_CSS + '</style></head>', 1)
    path.write_text(html, encoding='utf-8')
    print('updated', path)

print('done')
