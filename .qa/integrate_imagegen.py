"""Point chapter previews at the reviewed ImageGen assets already in the repo."""
import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
data_path = root / 'guide-data.js'
data = json.loads(data_path.read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
replacements = {}
assets = []
for chapter in data['chapters']:
    filename = f'ch{chapter["n"]:02d}-imagegen-20260915.png'
    relative = f'resources/chapter-mindmaps/{filename}'
    path = root / relative
    if not path.exists():
        continue
    with Image.open(path) as img:
        width, height = img.size
        assert width >= 1536 and height >= 1024, path
        img.verify()
    replacements[chapter['map'][len('resources/'):] ] = relative[len('resources/'):]
    chapter['map'] = chapter['generatedMap'] = relative
    assets.append({'chapter': chapter['n'], 'title': chapter['title'], 'file': filename,
                   'width': width, 'height': height,
                   'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

data_path.write_text('window.BOOK_DATA = '+json.dumps(data, ensure_ascii=False, indent=2)+';\n', encoding='utf-8')
updated = 0
for path in (root / 'resources').rglob('*.html'):
    before = path.read_text(encoding='utf-8')
    after = before
    for old, new in replacements.items():
        if old != new:
            updated += after.count(old)
            after = after.replace(old, new)
    if before != after:
        path.write_text(after, encoding='utf-8')

manifest = {'source': '70750 未转曲.pdf', 'sourcePages': 255,
            'sourceSha256': 'f7258b92156ec211ef7bcc80860fda7b4260b0d871f26ce72f10dbe756804a2e',
            'generator': 'imagegen', 'assets': assets}
(root/'resources/chapter-mindmaps/imagegen-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'imagegenChapters': len(assets), 'updatedPreviewReferences': updated}))
