#!/usr/bin/env python3
"""共享工作看板 — 服务器版（5003端口）

供笔记本/台式机双端浏览器共享查看：
- /dashboard (/) → 工作看板：项目进度 + 留言板动态 + 需要你裁决
- /architecture.html → 项目架构总览
- /guide.html → 操作指引

数据源：memory.db（与知识库同一份，靠 sync_kb 同步到服务器）
密码：KB_USER/KB_PASS 环境变量（与知识库一致，不设置则免密）
"""
import sqlite3, os
from pathlib import Path
from flask import Flask, request, Response

app = Flask(__name__, static_folder='.', static_url_path='')
MEM_DB = os.environ.get('MEM_DB', '/opt/local-memory/data/memory.db')
KB_USER = os.environ.get('KB_USER', '')
KB_PASS = os.environ.get('KB_PASS', '')
PORT = int(os.environ.get('PORT', '5003'))
SERVER = os.environ.get('SERVER_URL', 'http://106.53.70.121')


@app.before_request
def check_auth():
    if not KB_USER:
        return
    auth = request.authorization
    if not auth or auth.username != KB_USER or auth.password != KB_PASS:
        return Response('Login required', 401,
                        {'WWW-Authenticate': 'Basic realm="Dashboard"'})
    return None


@app.route('/')
@app.route('/dashboard')
def dashboard():
    try:
        mdb = sqlite3.connect(MEM_DB)
        mdb.row_factory = sqlite3.Row
        proj_rows = mdb.execute(
            "SELECT project, name, status, description FROM project_profile ORDER BY status, project").fetchall()
        proj_cards = ''
        owner_map = {'quant': '量化', 'recite-app': '量化', 'bili-fetcher': '量化', 'voice-workstation': '量化',
                     'mini-program': '养老', 'nursing': '养老',
                     'memory': '记忆', 'math-inverse': '记忆', 'knowledge-base': '记忆'}
        status_color = {'已上线': '#27ae60', '开发中': '#3498db', '备案中': '#f39c12',
                        '进行中': '#f39c12', '暂停': '#e74c3c'}
        if not proj_rows:
            proj_cards = '<div class="empty">暂无项目数据，各窗口用 <code>mem progress set</code> 添加</div>'
        for r in proj_rows:
            s = r['status']
            if not s:
                continue
            owner = owner_map.get(r['project'], '?')
            color = status_color.get(s, '#666')
            proj_cards += (f'<div class="card"><b>{r["name"] or r["project"]}</b> '
                           f'<span class="tag" style="background:{color}">{s}</span> '
                           f'<span class="time">{owner}</span>'
                           f'<div class="msg">{r["description"] or ""}</div></div>')
        dynamics = {}
        need_user = []
        for r in mdb.execute("SELECT id, sender, message, created_at FROM board WHERE status='pending' ORDER BY id DESC").fetchall():
            s = r['sender']
            if s not in dynamics:
                dynamics[s] = r
            if '@user' in r['message']:
                need_user.append(r)
        mdb.close()
    except Exception as e:
        dynamics = {}
        need_user = []
        proj_cards = f'<div class="empty">数据库错误: {e}</div>'

    dyn_html = (''.join(f'<div class="card"><span class="tag" style="background:#06c">{s}</span>'
                        f'<span class="time">{r["created_at"][:16]}</span>'
                        f'<div class="msg">{r["message"]}</div></div>'
                        for s, r in sorted(dynamics.items()))
                or '<div class="empty">暂无动态</div>')
    user_html = (''.join(f'<div class="card" style="border-left:3px solid #e74c3c">'
                         f'<span class="tag" style="background:#06c">{r["sender"]}</span>'
                         f'<span class="time">{r["created_at"][:16]}</span>'
                         f'<div class="msg">⚡ {r["message"]}</div></div>' for r in need_user)
                or '<div class="empty">全部已处理 ✅</div>')

    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>工作看板</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,sans-serif;background:#f5f7fb;padding:0;color:#333}}
h2{{font-size:.95rem;margin:1rem 0 .4rem;color:#333}}
.prow{{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.5rem}}
.pbtn{{flex:1;min-width:110px;color:#fff;text-align:center;padding:.7rem;border-radius:10px;text-decoration:none;font-size:.82rem;font-weight:600;box-shadow:0 2px 6px rgba(0,0,0,.1)}}
.header{{background:#fff;border-bottom:1px solid #eef0f4;padding:0 20px;height:48px;display:flex;align-items:center;justify-content:center;position:relative}}
.header .port{{position:absolute;right:20px;font-size:.72rem;color:#bbb}}
.header a{{padding:6px 14px;border-radius:6px;text-decoration:none;font-size:.82rem;color:#555;transition:.1s}}
.header a:hover{{background:#f0faf5;color:#42b983}}
.header a.cur{{background:#f0faf5;color:#42b983;font-weight:600}}
.header .gap{{flex:1}}
.card{{background:#fff;border-radius:10px;padding:.6rem .9rem;margin-bottom:.35rem;box-shadow:0 1px 3px rgba(0,0,0,.05);font-size:.85rem}}
.tag{{display:inline-block;color:#fff;font-size:.6rem;padding:.06rem .4rem;border-radius:4px;margin-right:.35rem;font-weight:600}}
.time{{font-size:.7rem;color:#999;float:right}}
.msg{{font-size:.82rem;margin-top:.25rem;line-height:1.5;color:#333}}
.empty{{text-align:center;padding:1.5rem;color:#999;font-size:.82rem}}
</style></head><body>
<div class="header">
  <span style="padding:6px 14px;border-radius:6px;font-size:.82rem;background:#f0faf5;color:#42b983;font-weight:600">📊 看板</span>
  <a href="{SERVER}:5003/architecture.html">📐 架构</a>
  <a href="{SERVER}:5003/guide.html">📖 指引</a>
  <a href="{SERVER}:5004/">📚 知识库</a>
  <span class="port">服务器共享看板</span>
</div>
<div style="max-width:700px;margin:0 auto;padding:16px 20px 40px">
<h2>📌 项目进度</h2>
{proj_cards}
<h2>☁️ 服务器部署</h2>
<div class="prow">
<a href="{SERVER}:5000/" target="_blank" class="pbtn" style="background:#27ae60">记单词</a>
<a href="{SERVER}:5004/" target="_blank" class="pbtn" style="background:#42b983">知识库</a>
<a href="{SERVER}:5005/" target="_blank" class="pbtn" style="background:#8b5cf6">护理备考</a>
<a href="{SERVER}:5212/" target="_blank" class="pbtn" style="background:#06c">网盘中转</a>
<a href="{SERVER}:8082/" target="_blank" class="pbtn" style="background:#f39c12">熊猫游戏</a>
</div>
<h2>💬 各窗口当前动态</h2>
{dyn_html}
<h2>⚡ 需要你裁决</h2>
{user_html}
<div class="footer" style="text-align:center;font-size:.7rem;color:#ccc;margin-top:1.5rem">刷新页面查看最新 · 数据随 memory.db 自动同步</div>
</div>
</body></html>'''


@app.route('/architecture.html')
def architecture():
    return app.send_static_file('architecture.html')


@app.route('/guide.html')
def guide():
    return app.send_static_file('guide.html')


if __name__ == '__main__':
    print(f'共享看板: http://localhost:{PORT} ({"密码保护" if KB_USER else "无密码"})')
    app.run(host='0.0.0.0', port=PORT, debug=False)
