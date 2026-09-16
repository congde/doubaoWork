#!/usr/bin/env python3
# Rebuild the skill kit page so copy, download, search, maps and chapter links all work.
from pathlib import Path
import re
import base64

root = Path('/workspace/doubaoWork')
src = root / 'resources/skill-kit/index.html'
text = src.read_text(encoding='utf-8')

skill_data = re.search(r'<script id="skill-data" type="application/json">.*?</script>', text, re.S).group(0)
all_zip = re.search(r'<script id="all-zip" type="application/octet-stream">.*?</script>', text, re.S).group(0)

# Persist the combined zip so the "download all" control is a real file link.
raw_zip = re.search(r'<script id="all-zip" type="application/octet-stream">(.*?)</script>', text, re.S).group(1)
pack_dir = root / 'resources/skill-kit/packs'
pack_dir.mkdir(exist_ok=True)
combined = pack_dir / 'all-skills.zip'
combined.write_bytes(base64.b64decode(raw_zip.strip()))

style = r'''
.wrap{max-width:1510px;margin:24px auto 0;padding:0 4vw 48px;display:grid;grid-template-columns:340px 1fr;gap:24px}
aside,.detail{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:22px}
aside{align-self:start}label{font-weight:600;display:block;margin-bottom:7px}
input,textarea{border:1px solid var(--line);border-radius:14px;padding:12px 16px;width:100%;color:var(--text);background:#fff}
textarea{resize:vertical;min-height:200px}
#list{margin-top:14px;display:grid;gap:6px;max-height:670px;overflow:auto}
.item{text-align:left;border:0;background:transparent;width:100%;padding:12px;line-height:1.5;display:block;border-radius:12px;color:var(--text)}
.item small{display:block;color:var(--muted)}.item[aria-current=true]{background:var(--soft);box-shadow:inset 3px 0 var(--accent)}
.detail h2{font-size:28px;margin:3px 0 10px;line-height:1.4;letter-spacing:-.4px}.meta{font-size:13px;color:var(--muted)}.summary{color:var(--muted)}
.tabs{display:flex;gap:8px;margin:24px 0 20px}
.tabs button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 16px;color:var(--muted)}
.tabs button[aria-pressed=true]{background:var(--soft);border-color:#afcae5;color:var(--text);font-weight:600}
.box{padding:18px 20px;background:#f4f8fc;border-radius:16px;margin:14px 0}.box p{margin:5px 0}
h3{font-size:17px;margin:0 0 9px}.actions{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}
.hint{color:var(--muted);font-size:13px}details{border-top:1px solid var(--line);margin-top:20px;padding-top:16px}
summary{cursor:pointer;color:var(--accent);font-weight:600}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.8 inherit}
#status{min-height:28px;color:var(--accent);font-weight:600}#fallback{margin:14px 0}
#empty{color:var(--muted)}button:disabled,a.btn[aria-disabled=true]{opacity:.6;cursor:default}
[hidden]{display:none!important}
#all-download{margin-top:14px;width:100%}
#copy-text{min-height:180px}
.fallback-bar{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
button.primary{min-height:44px}
@media(max-width:800px){.wrap{grid-template-columns:1fr;padding:0 20px 40px;margin-top:16px}#list{max-height:230px}.detail{padding:20px}.detail h2{font-size:24px}.tabs{margin-top:18px}}
'''

body = r'''<header class="top">
  <a class="brand" href="../../index.html">
    <div class="mark" aria-hidden="true">豆</div>
    <div><strong>豆包工作</strong><small>随书技能</small></div>
  </a>
  <div class="top-actions"><a href="../../index.html">返回阅读指南</a></div>
</header>
<div class="page-intro">
  <div class="eyebrow">随书技能</div>
  <h1>选一个任务，直接开始。</h1>
  <p>这里是随书技能。先用现成示例试一次，再换成自己的材料。复制后的完整指令可直接粘贴到 AI 对话。</p>
  <div class="steps"><span>① 选择任务</span><span>② 复制完整指令</span><span>③ 粘贴到 AI 对话</span></div>
</div>
<main class="wrap">
<aside>
  <label for="search">你想完成什么？</label>
  <input id="search" type="search" placeholder="搜索：纪要、周报、PPT、数据、文档……" autocomplete="off">
  <nav id="list" aria-label="选择章节技能"></nav>
  <p id="empty" hidden>没有找到。试试“纪要”“报告”“PPT”“表格”“调研”或章节编号。</p>
  <p class="hint">第一次使用推荐：会议纪要。</p>
  <a class="btn" id="all-download" href="packs/all-skills.zip" download="all-skills.zip">下载全部 15 个技能</a>
</aside>
<section class="detail" aria-label="技能使用区">
  <div id="chapter" class="meta"></div>
  <h2 id="title">正在载入技能……</h2>
  <p id="description" class="summary"></p>
  <div class="tabs" aria-label="使用方式">
    <button type="button" id="trial-tab" aria-pressed="true">先试一下</button>
    <button type="button" id="own-tab" aria-pressed="false">用我的材料</button>
  </div>
  <div id="trial-pane">
    <div class="box">
      <h3>示例已准备好</h3>
      <p id="sample"></p>
    </div>
    <p class="hint">按钮会生成技能规则和本次示例。复制后粘贴到 AI 对话即可发送。</p>
  </div>
  <div id="own-pane" hidden>
    <div class="box">
      <h3>准备这些材料</h3>
      <p id="inputs"></p>
    </div>
    <label for="materials">粘贴你的材料</label>
    <textarea id="materials" placeholder="把记录、资料或数据贴在这里。"></textarea>
    <label for="extra" style="margin-top:14px">补充要求（选填）</label>
    <input id="extra" placeholder="例如：面向项目负责人，控制在一页以内">
    <p class="hint">未填写的信息可以留空；关键材料不足时，AI会集中询问。输入只停留在本页，刷新或关闭前请复制保留。</p>
  </div>
  <div class="actions">
    <button type="button" id="copy" class="primary">复制示例，马上试用</button>
    <a class="btn" id="download" href="packs/">下载这个技能包</a>
  </div>
  <div id="status" role="status" aria-live="polite"></div>
  <div id="fallback" hidden>
    <label for="copy-text">完整任务指令（可直接全选复制到 AI 对话）</label>
    <div class="fallback-bar">
      <button type="button" id="select-all">全选指令</button>
    </div>
    <textarea id="copy-text" readonly></textarea>
  </div>
  <details><summary>完成后怎么检查？</summary><p id="expected"></p></details>
  <details><summary>会得到什么？需要哪些工具？</summary><p id="output"></p><p id="dependency"></p>
    <p class="hint">本页试用默认交付对话中的文本。若要实际文件，请在具备相应工具的环境中追加制作要求。</p>
  </details>
  <details><summary>查看完整技能规则</summary><pre id="rules"></pre></details>
  <details><summary>想把技能保存下来？</summary>
    <p>下载这个技能包，解压后打开“示例_复制即用.txt”即可试用。“我的任务_替换材料.txt”用于下次工作；技能文件也一并保存在包内，供支持技能的环境加载。也可打开 <a href="packs/">技能包目录</a> 直接取用 zip。</p>
  </details>
</section>
</main>
<footer class="footer">本页可离线使用，不上传材料，也不连接你的账号。下载包已包含使用说明和示例。</footer>
<noscript>
  <p class="footer">当前浏览器未启用脚本。请打开 <a href="packs/">skill packs</a> 获取 15 个技能包，或返回 <a href="../../index.html">阅读指南</a>。</p>
</noscript>
'''

script = r'''
'use strict';
const ALIAS = {
  1: '试点 筛选 文档 任务 清单 开始',
  2: '会议 纪要 文档 记录 第一次 上手 推荐',
  3: '任务书 需求 指令 验收 概念',
  4: '文档 报告 写作 材料 成稿 方案',
  5: 'PPT ppt 演示 汇报 页面 幻灯片',
  6: '表格 数据 订单 excel Excel 清洗 汇总 分析',
  7: '调研 择校 证据 研究 报告 检索',
  8: '浏览器 网页 电脑 登记 断点 操作',
  9: '定时 监控 自动化 竞品 周期 流程',
  10: '创意 海报 视频 图像 原型 内容',
  11: '飞书 团队 行动项 协作 连接',
  12: '周报 技能 复用 校验 生态',
  13: '安全 权限 隐私 授权 治理',
  14: '岗位 流程 场景 业务',
  15: '复盘 成效 试点 评估 未来'
};
const $ = id => document.getElementById(id);
let skills = [];
try {
  skills = JSON.parse($('skill-data').textContent);
} catch (err) {
  $('title').textContent = '技能数据未能加载';
  $('description').textContent = '请改用本页左侧的“下载全部 15 个技能”，或打开技能包目录。';
}
const drafts = new Map();
let selected = skills.find(s => s.n === chapterFromLocation()) || skills.find(s => s.n === 2) || skills[0];
let mode = 'trial';

function chapterFromLocation() {
  const hash = (location.hash || '').replace(/^#/, '');
  const query = new URLSearchParams(location.search);
  const raw = hash || query.get('n') || query.get('ch') || '';
  const found = String(raw).match(/(\d{1,2})/);
  return found ? Number(found[1]) : 2;
}
function haystack(s) {
  return ['第' + s.n + '章', String(s.n), s.name || '', s.title, s.description, s.sample, s.inputs, ALIAS[s.n] || ''].join(' ').toLowerCase();
}
function compose(s, materials, extra) {
  return '请使用下面的技能处理本次材料。材料足够时直接完成；缺少关键信息时集中询问。本次只交付对话中的文本结果，不外发、不创建定时任务、不修改外部系统。\n\n' + s.rules + '\n\n【本次材料】\n' + materials + (extra && extra.trim() ? '\n\n【补充要求】\n' + extra.trim() : '');
}
function currentText() {
  if (mode === 'trial') return selected.trial;
  return compose(selected, $('materials').value.trim(), $('extra').value);
}
function storeDraft() {
  if (!selected) return;
  drafts.set(selected.n, {materials: $('materials').value, extra: $('extra').value});
}
function bytesFromBase64(b64) {
  const bin = atob(String(b64 || '').replace(/\s+/g, ''));
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
function triggerBlobDownload(bytes, filename) {
  const url = URL.createObjectURL(new Blob([bytes], {type: 'application/zip'}));
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}
function packHref(filename) {
  return 'packs/' + encodeURIComponent(filename);
}
function syncHash() {
  if (!selected) return;
  const next = '#ch' + selected.n;
  if (location.hash !== next) {
    try { history.replaceState(null, '', next); } catch (e) {}
  }
}
function score(s, q) {
  if (!s) return 0;
  if (!q) return 1;
  const title = ('第' + s.n + '章 ' + s.title + ' ' + (s.name || '') + ' ' + (ALIAS[s.n] || '')).toLowerCase();
  if (/^\d{1,2}$/.test(q) && String(s.n) === q) return 3;
  if (title.includes(q)) return 2;
  if (haystack(s).includes(q)) return 1;
  return 0;
}
function list() {
  const q = $('search').value.trim().toLowerCase();
  $('list').replaceChildren();
  let count = 0;
  const ordered = skills.slice().sort((a, b) => score(b, q) - score(a, q) || a.n - b.n);
  for (const s of ordered) {
    if (q && !score(s, q)) continue;
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'item';
    b.setAttribute('aria-current', String(selected && s.n === selected.n));
    const n = document.createElement('small');
    n.textContent = '第 ' + s.n + ' 章';
    const t = document.createElement('span');
    t.textContent = s.title;
    b.append(n, t);
    b.addEventListener('click', () => {
      storeDraft();
      selected = s;
      render();
    });
    $('list').append(b);
    count++;
  }
  $('empty').hidden = count !== 0;
}
function setMode(value) {
  mode = value;
  $('trial-pane').hidden = value !== 'trial';
  $('own-pane').hidden = value !== 'own';
  $('trial-tab').setAttribute('aria-pressed', String(value === 'trial'));
  $('own-tab').setAttribute('aria-pressed', String(value === 'own'));
  $('copy').textContent = value === 'trial' ? '复制示例，马上试用' : '复制完整任务指令';
  $('status').textContent = '';
}
function render() {
  if (!selected) return;
  for (const key of ['title', 'description', 'sample', 'inputs', 'expected', 'output', 'dependency', 'rules']) {
    $(key).textContent = selected[key] || '';
  }
  $('chapter').textContent = '随书技能';
  $('download').href = packHref(selected.filename);
  $('download').setAttribute('download', selected.filename);
  const d = drafts.get(selected.n) || {materials: '', extra: ''};
  $('materials').value = d.materials;
  $('extra').value = d.extra;
  $('fallback').hidden = true;
  $('copy-text').value = '';
  setMode(mode);
  syncHash();
  list();
}
function showInstruction(text, copied) {
  $('copy-text').value = text;
  $('fallback').hidden = false;
  $('copy-text').focus();
  $('copy-text').select();
  $('status').textContent = copied
    ? '已复制。打开 AI 对话，粘贴后直接发送。'
    : '完整指令已显示在下方，请全选复制后粘贴到 AI 对话。';
}
function copyInstruction() {
  if (!selected) return;
  if (mode === 'own' && !$('materials').value.trim()) {
    $('status').textContent = '先贴入你的材料，再复制任务指令。';
    $('materials').focus();
    return;
  }
  const text = currentText();
  showInstruction(text, false);
  const markCopied = () => { $('status').textContent = '已复制。打开 AI 对话，粘贴后直接发送。'; };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(markCopied).catch(() => {
      try { if (document.execCommand('copy')) markCopied(); } catch (e) {}
    });
    return;
  }
  try { if (document.execCommand('copy')) markCopied(); } catch (e) {}
}
function downloadEmbedded(event, b64, filename) {
  if (location.protocol !== 'file:') return;
  event.preventDefault();
  triggerBlobDownload(bytesFromBase64(b64), filename);
}
$('search').addEventListener('input', list);
$('trial-tab').addEventListener('click', () => setMode('trial'));
$('own-tab').addEventListener('click', () => setMode('own'));
$('copy').addEventListener('click', copyInstruction);
$('select-all').addEventListener('click', () => {
  if (!$('copy-text').value) $('copy-text').value = selected ? currentText() : '';
  $('fallback').hidden = false;
  $('copy-text').focus();
  $('copy-text').select();
});
$('download').addEventListener('click', event => {
  if (!selected) return;
  downloadEmbedded(event, selected.zip, selected.filename);
  $('status').textContent = '已发起下载；解压后打开 README.txt。';
});
$('all-download').addEventListener('click', event => {
  downloadEmbedded(event, $('all-zip').textContent.trim(), 'all-skills.zip');
  $('status').textContent = '已发起整套下载，请到浏览器下载记录查看。';
});
window.addEventListener('hashchange', () => {
  const next = skills.find(s => s.n === chapterFromLocation());
  if (!next || (selected && next.n === selected.n)) return;
  storeDraft();
  selected = next;
  render();
});
if (selected) render();
'''

html = (
    '<!doctype html>\n'
    '<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>章节技能 · 选一个任务，直接开始</title>\n'
    '<link rel="stylesheet" href="../../site.css">\n'
    '<style>' + style + '</style></head><body>\n'
    + body + '\n'
    + skill_data + '\n'
    + all_zip + '\n'
    + '<script>' + script + '</script></body></html>\n'
)

kit = root / 'resources/skill-kit/index.html'
kit.write_text(html, encoding='utf-8')
print('wrote', kit, 'bytes', kit.stat().st_size)

# Keep the companion copy working: its zip packs live in the kit folder.
companion = root / 'resources/companion/index.html'
companion.write_text(
    html.replace('href="packs/', 'href="../skill-kit/packs/')
        .replace("return 'packs/' + encodeURIComponent(filename);",
                 "return '../skill-kit/packs/' + encodeURIComponent(filename);"),
    encoding='utf-8'
)
print('wrote', companion, 'bytes', companion.stat().st_size)
print('combined zip', combined, combined.stat().st_size)
