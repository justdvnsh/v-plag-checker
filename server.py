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
from ngram import find_similarity_n_grams
import json
from detect import detect

__author__ = 'Divyansh'

CONFIG_FILE_NAME = 'lmf.yml'
projects = {}

app = connexion.App(__name__, debug=False)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Project:
    def __init__(self, LM, config):
        self.config = config
        self.lm = LM()


# # def get_all_projects():
# #     res = {}
# #     for k in projects.keys():
# #         res[k] = projects[k].config
# #     return res

# # ##def copylinks

# # def analyze(analyze_request):
# #     project = analyze_request.get('project')
# #     text = analyze_request.get('text')

# #     res = {}
# #     if project in projects:
# #         p = projects[project] # type: Project
# #         res = p.lm.check_probabilities(text, topk=20)

# #     return {
# #         "request": {'project': project, 'text': text},
# #         "result": res
# #     }

# print(projects)

# @app.route('/validate', methods=['POST'])
# def validate():
#     text = request.form['text']

#     return "You Entered : {}".format(text)

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
    # lm = LM()
    for _,_,files in os.walk('uploads'):
        for file in files:
            files_uploaded.append(file)

    if len(files_uploaded) > 0:
        for i in range(len(files_uploaded)):
            if i == len(files_uploaded) - 1:
                break
            else:
                ## checking the n-gram similarity
                data['files_' + files_uploaded[0] + '_' + files_uploaded[i+1]] = find_similarity_n_grams(files_uploaded[0], files_uploaded[i+1])

        for i in range(len(files_uploaded)):
            data['file_' + files_uploaded[i]] = detect(file=files_uploaded[i])
    else:
        data[text] = text
        data['text_score'] = detect(text=text)

    for _,_,files in os.walk('uploads'):
        for file in files:
            os.remove('uploads/' + file)    
    #result = 'The result is {}'.format(data)
    # payload = lm.check_probabilities(text)
    # payload = payload['pred_topk'].apply(lambda x: x.slice(0, 10))
    return render_template('result.html', data=data)
    

# app.add_api('server.yaml')

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
