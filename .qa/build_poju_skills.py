#!/usr/bin/env python3
# Split 破局Skill.zip into one zip per skill and write poju-data.js
import json
import re
import zipfile
from pathlib import Path

root = Path('/workspace/doubaoWork')
src_zip = root / 'resources/skill-kit/破局Skill.zip'
catalog_html = root / 'resources/skill-kit/poju-catalog.html'
pack_dir = root / 'resources/skill-kit/packs'
data_js = root / 'poju-data.js'
SKIP = {'_catalog.json', '_report.json', 'index.html'}


def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = (s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
         .replace('&quot;', '"').replace('&#39;', "'"))
    return re.sub(r'\s+', ' ', s).strip()


def norm(s):
    return re.sub(r'[\s·_/（）()【】\[\]\-]+', '', s).lower()


def parse_catalog(html):
    rows = re.findall(
        r'<tr[^>]*>\s*<td class="cat"[^>]*>(.*?)</td>\s*<td class="name"[^>]*>(.*?)</td>'
        r'\s*<td class="sum"[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td class="num"[^>]*>(.*?)</td>',
        html, re.S)
    items = []
    for cat, name, summ, author, num in rows:
        items.append({
            'cat': clean(cat),
            'name': clean(name),
            'brief': clean(summ),
            'author': clean(author),
            'files': int(clean(num) or 0),
        })
    return items


def slug(folder, n):
    safe = re.sub(r'[^\w\u4e00-\u9fff\-]+', '-', folder).strip('-')
    return '%03d-%s' % (n, safe[:48])


def main():
    catalog = parse_catalog(catalog_html.read_text(encoding='utf-8'))
    pack_dir.mkdir(parents=True, exist_ok=True)
    for old in pack_dir.glob('ch*.zip'):
        old.unlink()
    all_old = pack_dir / 'all-skills.zip'
    if all_old.exists():
        all_old.unlink()

    with zipfile.ZipFile(src_zip) as z:
        names = [n.replace('\\', '/') for n in z.namelist()]
        tops = sorted({n.split('/')[0] for n in names if n.split('/')[0] and n.split('/')[0] not in SKIP})
        zmap = {norm(t): t for t in tops}
        groups = {}
        for name in names:
            top = name.split('/')[0]
            if top in SKIP:
                continue
            groups.setdefault(top, []).append(name)

        out = []
        for i, item in enumerate(catalog, 1):
            folder = zmap.get(norm(item['name']))
            if not folder:
                raise SystemExit('no folder for %s' % item['name'])
            zip_name = slug(folder, i) + '.zip'
            dest = pack_dir / zip_name
            with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED) as outz:
                for inner in groups.get(folder, []):
                    info = z.getinfo(inner)
                    data = z.read(inner)
                    # keep files under the skill folder name
                    outz.writestr(inner, data, compress_type=zipfile.ZIP_DEFLATED)
            out.append({
                'n': i,
                'id': 'poju-%03d' % i,
                'name': item['name'],
                'cat': item['cat'],
                'brief': item['brief'],
                'author': item['author'],
                'folder': folder,
                'zip': 'resources/skill-kit/packs/' + zip_name,
                'page': 'resources/skill-kit/index.html#' + ('poju-%03d' % i),
            })
            print('%03d %s -> %s (%d bytes)' % (i, item['name'], zip_name, dest.stat().st_size))

    data_js.write_text(
        'window.POJU_SKILLS = ' + json.dumps(out, ensure_ascii=False, indent=2) + ';\n',
        encoding='utf-8'
    )
    print('wrote', data_js, 'skills', len(out), 'packs', len(list(pack_dir.glob('*.zip'))))


if __name__ == '__main__':
    main()
