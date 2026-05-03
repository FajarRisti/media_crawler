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

@app.route('/run', methods=['POST'])
def run_crawler():
    keyword = request.form.get('keyword', 'python')
    start_date = request.form.get('start_date', '')
    end_date = request.form.get('end_date', '')
    
    cmd = ['python', 'main_fast.py', keyword]
    if start_date:
        cmd += ['--start-date', start_date]
    if end_date:
        cmd += ['--end-date', end_date]
    
    def run():
        subprocess.run(cmd, capture_output=True, text=True)
    
    thread = threading.Thread(target=run)
    thread.start()
    params = f'"{keyword}" {start_date or "no"} {end_date or "no"}'
    return f'Crawler started: {params}'

@app.route('/clear', methods=['POST'])
def clear():
    if os.path.exists('data.json'):
        open('data.json', 'w').write('[]')
    return 'Cleared!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
