#!/usr/bin/env python3
"""添加量化窗口负责的项目到知识库"""
import sqlite3

DB = 'd:/code/local-memory/data/memory.db'
db = sqlite3.connect(DB)

projects = [
    ('recite-app', '记单词 App', 'Flask+SQLite H5单词记忆应用，遗忘曲线+多词库+管理面板',
     'Flask/SQLite/Pico.css', 'Flask', 'SQLite (recite.db)',
     '4544 CET-4 + 8个年级PEP词库'),
    ('bili-fetcher', 'Bili-Fetcher (B站爬取转写)', 'B站视频下载+Whisper转写+内容分析',
     'Python/yt-dlp/faster-whisper', 'Python CLI', 'SQLite',
     '32个魔神视频已转写+27篇分析'),
    ('voice-workstation', '口播工作站', '语音合成工具',
     'Python/Flask', 'Flask', '本地文件',
     '已开发完'),
    ('knowledge-base', '知识库', '跨项目经验文档站，汇总经验+项目档案',
     'Python/Flask/marked.js', 'Flask', 'local-memory SQLite',
     '汇总所有窗口经验'),
]

for p in projects:
    db.execute('''INSERT OR IGNORE INTO project_profile
        (project, name, description, tech_stack, framework, database_info, key_params)
        VALUES (?,?,?,?,?,?,?)''', p)
    print(f'Project: {p[0]}')

knowledge = [
    ('pa_recite', '记单词 App - 项目概述',
     '# 记单词 App\n\n## 简介\nFlask+SQLite 单词记忆 H5，遗忘曲线+多词库+管理面板\n\n## 功能\n- 遗忘曲线 T0-T5，可自定义间隔\n- 多词库: CET-4(4544词) + 8个年级PEP词库\n- 例句补全全部覆盖\n- 排行榜所有用户可见\n- 管理面板: 密码重置/清空数据\n\n## 技术\n- Flask + SQLite / Pico.css 纯H5\n- 部署: 106.53.70.121:5000\n- Git: github.com/wuyfer365/recite-app',
     'recite-app,flask,单词'),

    ('pa_bili', 'Bili-Fetcher - 项目概述',
     '# Bili-Fetcher\n\nB站视频下载 + faster-whisper 转写\n\n## 状态\n- 32个魔神视频全部转写完成\n- 27篇分析文档\n- 已基于魔神哲学设计量化策略',
     'bili,whisper,B站'),

    ('pa_voice', '口播工作站 - 项目概述',
     '# 口播工作站\n\n语音合成工具，将文本转为语音。\n\n## 状态\n已开发完。',
     'voice,tts'),

    ('pa_kb', '知识库 - 项目概述',
     '# 知识库\n\n跨项目经验文档站，汇总各窗口经验和项目档案。\n\n## 技术\n- Flask + marked.js\n- 数据源: local-memory SQLite',
     'knowledge-base,文档'),

    ('pt_recite', '记单词 App - 踩坑总结',
     '## 1. 弹窗按钮 onclick 被覆盖\nshowPrompt 修改弹窗按钮 onclick 未恢复，后续 showConfirm 按钮失效。\n修复: showModal/showConfirm 中显式绑定 confirmOk\n\n## 2. 清空数据后 stats 仍显示旧数据\nlocation.reload() 过程中后台 fetch 把旧数据写回 localStorage。\n修复: 清除缓存 + ?cleared= URL 参数跳过缓存\n\n## 3. API 参数顺序错误\nCategories API params=[topic_id,diff] 写反导致过滤后空数组。\n修复: 改为 params=[diff,topic_id]',
     'recite-app,bug'),

    ('pt_kb', '知识库 - 踩坑总结',
     '## 1. CDN 被拦截导致页面空白\nmarked.min.js 从 CDN 加载被浏览器跟踪防护拦截。\n修复: 下载到本地引用\n\n## 2. Python 模板字符串转义问题\nHTML 中 script 标签在 Python 字符串中需转义。\n修复: 改用独立 index.html + send_static_file',
     'knowledge-base,cdn'),
]

for k in knowledge:
    db.execute('''INSERT OR IGNORE INTO knowledge (node_id, title, content, tags)
        VALUES (?,?,?,?)''', k)
    print(f'Knowledge: {k[0]}')

db.commit()
db.close()
print('Done!')
