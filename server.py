#!/usr/bin/env python3
"""知识库 — Flask 文档站"""
import sqlite3, json, time, os
from pathlib import Path
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')
BASE = Path(__file__).parent
MEM_DB = BASE.parent / 'local-memory' / 'data' / 'memory.db'

@app.route('/api/knowledge-data')
def api_data():
    p=[];e=[];k=[]
    try:
        db=sqlite3.connect(str(MEM_DB));db.row_factory=sqlite3.Row
        for r in db.execute("SELECT project,name,description FROM project_profile ORDER BY project").fetchall(): p.append(dict(r))
        for r in db.execute("SELECT window,date,problem,root_cause,solution,tech_stack,project FROM experience ORDER BY date DESC LIMIT 200").fetchall(): e.append(dict(r))
        for r in db.execute("SELECT node_id,title,content FROM knowledge").fetchall(): k.append(dict(r))
        db.close()
    except: pass
    return jsonify({'projects':p,'experiences':e,'knowledge':k})

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    print('http://localhost:5004')
    app.run(host='0.0.0.0', port=5004, debug=True)
