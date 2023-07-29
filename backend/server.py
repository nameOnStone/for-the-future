# save this as app.py

import os
import sys
import re
import time
import glob
import json
import pdb
from flask_cors import CORS
# from celery import Celery
#from memory_profiler import profile
#from flask_httpauth import HTTPBasicAuth
from flask import Flask, escape, request, jsonify, send_from_directory, make_response, render_template, url_for, current_app
#from gevent import pywsgi
#import psutil

import get_rangeline_from_file

from tsv2json.core import TSV

global binpath

binpath = sys.path[0]
db = 'db'

app = Flask(__name__, template_folder="./dist", static_folder="./dist/static", static_url_path="")
app.config['SECRET_KEY'] = 'top-secret!'

CORS(app, resources=r"/*")

# @app.route("/index")
# def index():
#     return render_template("index.html")


@app.route("/db/test")
def fetchTest():
    tpmfile = f"db/stock_list.20230728.xls"
    print("-->", tpmfile)
    data = get_rangeline_from_file.main(tpmfile, 0, 1)
    alldata = get_rangeline_from_file.main(tpmfile, 0, data['dataCount']+10)
    return alldata["trunk_data"]


@app.route("/view/tpm/<sample>/searching")
def getTPMsearchingGenename(sample):
    tpmfile = f"{dbSamples}/{sample}.featurecount.gene_id.tpm.txt"
    gene_id = request.args.get("gene_id")
    data = get_rangeline_from_file.main(tpmfile, 0, 1)
    alldata = get_rangeline_from_file.main(tpmfile, 0, data['dataCount']+10)
    mem = []
    for ele in alldata['trunk_data']:
        if ele["gene_id"] == gene_id:
            mem.append(ele)
    return {"trunk_data": mem, "dataCount": len(mem)}


if __name__ == "__main__":
    #server = pywsgi.WSGIServer(('192.168.1.97', 9999), app)
    #server.serve_forever()
    #os.system(redis_CMD)
    #os.system(f"./{celery_CMD} -A {binpath}/service.py worker -l info")
    app.run(host='172.19.154.77', port=9999, debug=True)
#    from waitress import serve
#    serve(app, host="192.168.1.97", port=9999)

#celery_CMD = f"{binpath}/celery/bin/celery"
#redis_CMD = f"{binpath}/redis-stable/bin/redis-server"
# elery configuration
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
#celery.conf.update(app.config)