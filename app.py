import json
from flask import Flask, jsonify, request
import os
import subprocess
import threading
import time
import argparse  # for main.py compatibility

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/data.json')
def data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/progress')
def progress():
    if os.path.exists('crawler.log'):
        with open('crawler.log', 'r') as f:
            return f.read()
    return 'No progress yet\n'

@app.route('/run', methods=['POST'])
def run_crawler():
    keyword = request.form.get('keyword', 'python')
    start_date = request.form.get('start_date', '')
    end_date = request.form.get('end_date', '')
    
    cmd = ['python', 'main_fast.py', keyword, '>' , 'crawler.log', '2>&1']
    if start_date:
        cmd += ['--start-date', start_date]
    if end_date:
        cmd += ['--end-date', end_date]
    
    def run():
        subprocess.run(cmd, shell=True)
    
    thread = threading.Thread(target=run)
    thread.start()
    return f'Crawler started: main_fast.py {keyword} → check /progress'

@app.route('/clear', methods=['POST'])
def clear():
    if os.path.exists('data.json'):
        open('data.json', 'w').write('[]')
    return 'Cleared!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
