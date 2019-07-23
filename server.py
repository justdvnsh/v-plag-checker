#!/usr/bin/env python

import argparse
import connexion
import os
import yaml
from flask import send_from_directory, redirect, request, render_template, jsonify
from flask_cors import CORS
# from backend.Project import Project # TODO !!
from backend import AVAILABLE_MODELS
from backend.api import LM
import time
from backend.utils.ngram import find_similarity_n_grams
import json
from backend.utils.detect import detect
from backend.utils.plag import plag_for_file, plag_for_text

__author__ = 'Divyansh'

CONFIG_FILE_NAME = 'lmf.yml'
projects = {}

app = connexion.App(__name__, debug=False)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Project:
    def __init__(self, LM, config):
        self.config = config
        self.lm = LM()

#########################
#  some non-logic routes
#########################

@app.route('/')
def redir():

    return redirect('client/fun.html')


@app.route('/client/<path:path>')
def send_static(path):
    """ serves all files from ./client/ to ``/client/<path:path>``

    :param path: path from api call
    """
    return send_from_directory('client/dist/', path)


@app.route('/data/<path:path>')
def send_data(path):
    """ serves all files from the data dir to ``/data/<path:path>``

    :param path: path from api call
    """
    print('Got the data route for', path)
    return send_from_directory(args.dir, path)

@app.route('/upload-target', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'uploads/')
    for file in request.files.getlist('file'):
        filename = file.filename
        print(filename)
        dest = "/".join([target, filename])
        file.save(dest)

    return 'YOUR FILE HAS BEEN SAVED'        

@app.route('/check-plag', methods=['POST'])
def check_plag():
    text = request.form['area']
    files_uploaded = []
    data = {}

    for _,_,files in os.walk('uploads'):
        for file in files:
            files_uploaded.append(file)

    if len(files_uploaded) > 0:
        if len(files_uploaded) > 1:
            for i in range(len(files_uploaded)):
                if i == len(files_uploaded) - 1:
                    break
                else:
                    ## checking the n-gram similarity
                    data['files_' + files_uploaded[0] + '_' + files_uploaded[i+1]] = find_similarity_n_grams(files_uploaded[0], files_uploaded[i+1])

        ## Check the ngram similarity and the AI plagiaism

        for i in range(len(files_uploaded)):
            data['file_ai_plag_' + files_uploaded[i]] = detect(file=files_uploaded[i])
            #data['file_plag_' + files_uploaded[i]] = plag_for_file(files_uploaded[i])
    else:
        data[text] = text
        data['text_score_ai_plag'] = detect(text=text)
        # data['text_score_plag'] = plag_for_text(text)

    for _,_,files in os.walk('uploads'):
        for file in files:
            os.remove('uploads/' + file)    
    
    return jsonify(data)
    
parser = argparse.ArgumentParser()
parser.add_argument("--model", default='gpt-2-small')
parser.add_argument("--nodebug", default=False)
parser.add_argument("--address",
                    default="127.0.0.1")  # 0.0.0.0 for nonlocal use
parser.add_argument("--port", default="5001")
parser.add_argument("--nocache", default=False)
parser.add_argument("--dir", type=str, default=os.path.abspath('data'))

parser.add_argument("--no_cors", action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()

    if not args.no_cors:
        CORS(app.app, headers='Content-Type')

    app.run(port=int(args.port), debug=not args.nodebug, host=args.address)
else:
    args, _ = parser.parse_known_args()
    # load_projects(args.dir)
    try:
        model = AVAILABLE_MODELS[args.model]
    except KeyError:
        print("Model {} not found. Make sure to register it.".format(
            args.model))
        print("Loading GPT-2 instead.")
        model = AVAILABLE_MODELS['gpt-2']
    projects[args.model] = Project(model, args.model)
