"""Собирает index.html из posts.md.
Формат posts.md: каждый пост начинается со строки "=== Название".
**жирный**, _курсив_; пустая строка = абзац."""
import html, re

src = open('posts.md', encoding='utf-8').read()
blocks = [b for b in re.split(r'^=== ', src, flags=re.M) if b.strip()]

def fmt(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w/])_(.+?)_(?![\w])', r'<i>\1</i>', s)
    s = re.sub(r'(https?://[^\s<]+)', r'<a href="\1">\1</a>', s)
    return s

cards = []
for i, b in enumerate(reversed(blocks)):  # новые сверху
    title, _, body = b.partition('\n')
    paras = [p.strip('\n') for p in body.strip().split('\n\n')]
    inner = '<br><br>'.join(fmt(p).replace('\n', '<br>') for p in paras)
    cards.append(f'<div class="lbl">{html.escape(title.strip())}</div>'
                 f'<button class="cp" onclick="cp(this)">📋 Скопировать пост</button>'
                 f'<div class="post">{inner}</div>')

page = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Посты ЛэшФая 2027</title>
<style>
body{{font-family:-apple-system,system-ui,sans-serif;font-size:17px;line-height:1.45;max-width:560px;margin:24px auto;padding:0 16px;background:#fff;color:#111}}
h1{{font-size:22px}}.post{{border:1px solid #ddd;border-radius:12px;padding:16px;margin:0 0 36px}}
.lbl{{font-size:12px;color:#999;text-transform:uppercase;letter-spacing:.08em;margin:0 0 8px}}
.cp{{display:block;width:100%;padding:14px;margin:0 0 10px;border:0;border-radius:10px;background:#111;color:#fff;font-size:16px;font-weight:600}}
.cp.ok{{background:#2e7d32}}a{{color:#111}}
</style></head><body>
<h1>Посты канала «ЛэшФая 2027 Москва»</h1>
<p style="color:#888;font-size:14px">Новые посты сверху. Кнопка копирует пост с абзацами, жирным и курсивом.</p>
{"".join(cards)}
<script>
function done(b){{b.textContent='✅ Скопировано';b.classList.add('ok');setTimeout(function(){{b.textContent='📋 Скопировать пост';b.classList.remove('ok')}},1800)}}
function sel(el){{var r=document.createRange();r.selectNodeContents(el);var s=window.getSelection();s.removeAllRanges();s.addRange(r);try{{document.execCommand('copy')}}catch(e){{}}s.removeAllRanges()}}
function cp(b){{var el=b.nextElementSibling;if(window.ClipboardItem&&navigator.clipboard&&navigator.clipboard.write){{navigator.clipboard.write([new ClipboardItem({{'text/html':new Blob([el.innerHTML],{{type:'text/html'}}),'text/plain':new Blob([el.innerText],{{type:'text/plain'}})}})]).then(function(){{done(b)}},function(){{sel(el);done(b)}})}}else{{sel(el);done(b)}}}}
</script></body></html>
'''
open('index.html', 'w', encoding='utf-8').write(page)
print(len(blocks), 'posts')
