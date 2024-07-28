
from flask import Flask, render_template,jsonify,request
from gevent import pywsgi
from loguru import logger
from datetime import datetime
import ujson as json
import os
from .env_check import get_env

app = Flask(__name__)

source_path,target_backup_path,keeptime,webport=get_env()

@app.route('/')
def hello_world():
    output = {}
    with open(os.path.join(os.getcwd(),'logs',(datetime.today()).strftime("%Y-%m-%d")+'.log'),'r',encoding='UTF-8') as f:
        data = f.readlines()
        
    n = 0
    
    for i in data:
        n += 1
        output.update({n:i.replace('\n','')})
        
    return jsonify(output)

@app.route('/log', methods=['GET'])  
def handle_log_request():
    param = str(request.args.get('param')).upper()
    
    try:
        
        output = {}
        
        with open(os.path.join(os.getcwd(),'logs',param+'.log'),'r',encoding='UTF-8') as f:
            data = f.readlines()
            
        n = 0
        
        for i in data:
            n += 1
            output.update({n:i.replace('\n','')})
            
        return jsonify(output)
    
    except Exception as e:
        
        return f"Error: {e}"
    
@app.route('/hash', methods=['GET'])  
def handle_hash_request():
    param = str(request.args.get('param')).upper()
    
    try:
        
        with open(os.path.join(target_backup_path,param,'hash.json'),'r',encoding='UTF-8') as f:
            output = json.load(f)
            
        return jsonify(output)
    
    except Exception as e:
        
        return f"Error: {e}"

def web_start(webport: int):
    # app.run(host='0.0.0.0', port=webport, debug=True)
    server = pywsgi.WSGIServer(('0.0.0.0',webport),app)
    server.serve_forever()