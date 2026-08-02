#!/usr/bin/env python3
"""知识库 — Flask 文档站（支持服务器部署 + 密码访问）

本地运行:  python server.py            → http://localhost:5004 无密码
服务器运行: 设置环境变量后再启动         → 需输入 KB_USER/KB_PASS 密码
  KB_USER=kb KB_PASS=xxxx PORT=5004 KB_DEBUG=0 python server.py
"""
import sqlite3, json, os
from pathlib import Path
from flask import Flask, jsonify, request, Response

app = Flask(__name__, static_folder='.', static_url_path='')
BASE = Path(__file__).parent
MEM_DB = BASE.parent / 'local-memory' / 'data' / 'memory.db'

# 部署配置（环境变量控制，本地不设置则无需密码）
KB_USER = os.environ.get('KB_USER', '')
KB_PASS = os.environ.get('KB_PASS', '')
PORT = int(os.environ.get('PORT', '5004'))
DEBUG = os.environ.get('KB_DEBUG', '') == '1'


@app.before_request
def check_auth():
    """设置了 KB_USER/KB_PASS 才启用 HTTP Basic Auth"""
    if not KB_USER:
        return
    auth = request.authorization
    if not auth or auth.username != KB_USER or auth.password != KB_PASS:
        # realm 必须 ASCII，中文会破坏 HTTP 头导致连接被断开
        return Response('Login required', 401,
                        {'WWW-Authenticate': 'Basic realm="Knowledge Base"'})
    return None


@app.route('/api/knowledge-data')
def api_data():
    p = []; e = []; k = []
    try:
        db = sqlite3.connect(str(MEM_DB))
        db.row_factory = sqlite3.Row
        for r in db.execute("SELECT project,name,description FROM project_profile ORDER BY project").fetchall():
            p.append(dict(r))
        for r in db.execute("SELECT window,date,problem,root_cause,solution,tech_stack,project FROM experience ORDER BY date DESC LIMIT 200").fetchall():
            e.append(dict(r))
        for r in db.execute("SELECT node_id,title,content FROM knowledge").fetchall():
            k.append(dict(r))
        db.close()
    except Exception as ex:
        print('DB read error:', ex)
    return jsonify({'projects': p, 'experiences': e, 'knowledge': k})


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    print('知识库: http://localhost:%d%s' % (PORT, ' (密码保护)' if KB_USER else ' (无密码)'))
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
