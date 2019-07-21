#!/usr/bin/env python

import argparse
import connexion
import os
import yaml
from flask import send_from_directory, redirect, request, render_template
from flask_cors import CORS
from copyleaks.copyleakscloud import CopyleaksCloud
from copyleaks.product import Product
from copyleaks.processoptions import ProcessOptions
# from backend.Project import Project # TODO !!
from backend import AVAILABLE_MODELS
import time
from ngram import find_similarity_n_grams
import json

__author__ = 'Divyansh'

CONFIG_FILE_NAME = 'lmf.yml'
projects = {}

app = connexion.App(__name__, debug=False)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

cloud = CopyleaksCloud(Product.Education, 'justdvnsh2208@gmail.com', 'cf6f8994-89bc-438b-a721-8ef3b912036f')

options = ProcessOptions()
options.setSandboxMode(True)  # Scan will not consume any credits and will return dummy results.
class Project:
    def __init__(self, LM, config):
        self.config = config
        self.lm = LM()


def get_all_projects():
    res = {}
    for k in projects.keys():
        res[k] = projects[k].config
    return res

##def copylinks

def analyze(analyze_request):
    project = analyze_request.get('project')
    text = analyze_request.get('text')

    res = {}
    if project in projects:
        p = projects[project] # type: Project
        res = p.lm.check_probabilities(text, topk=20)

    return {
        "request": {'project': project, 'text': text},
        "result": res
    }


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


    for i in range(len(files_uploaded)):
        if i == len(files_uploaded) - 1:
            break
        else:
            data['files_' + files_uploaded[0] + '_' + files_uploaded[i+1]] = find_similarity_n_grams(files_uploaded[0], files_uploaded[i+1])
    
    #result = 'The result is {}'.format(data)

    return render_template('index.html', data=data)
    


# @app.route('/')
# def redirect_home():
#     return redirect('/client/index.html', code=302)


# def load_projects(directory):
#     """
#     searches for CONFIG_FILE_NAME in all subdirectories of directory
#     and creates data handlers for all of them
#
#     :param directory: scan directory
#     :return: null
#     """
#     project_dirs = []
#     for root, dirs, files in walklevel(directory, level=2):
#         if CONFIG_FILE_NAME in files:
#             project_dirs.append(root)
#
#     i = 0
#     for p_dir in project_dirs:
#         with open(os.path.join(p_dir, CONFIG_FILE_NAME), 'r') as yf:
#             config = yaml.load(yf)
#             dh_id = os.path.split(p_dir)[1]
#             projects[dh_id] = Project(config=config, project_dir=p_dir,
#                                       path_url='data/' + os.path.relpath(p_dir,
#                                                                          directory))
#         i += 1
#
#
# # https://stackoverflow.com/a/234329/265298
# def walklevel(some_dir, level=1):
#     some_dir = some_dir.rstrip(os.path.sep)
#     assert os.path.isdir(some_dir)
#     num_sep = some_dir.count(os.path.sep)
#     for root, dirs, files in os.walk(some_dir):
#         yield root, dirs, files
#         num_sep_this = root.count(os.path.sep)
#         if num_sep + level <= num_sep_this:
#             del dirs[:]


app.add_api('server.yaml')

parser = argparse.ArgumentParser()
parser.add_argument("--model", default='gpt-2-small')
parser.add_argument("--nodebug", default=True)
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

    # cloud = CopyleaksCloud(Product.Education, 'justdvnsh2208@gmail.com', 'cf6f8994-89bc-438b-a721-8ef3b912036f')

    # options = ProcessOptions()
    # options.setSandboxMode(True)  # Scan will not consume any credits and will return dummy results.
    # print("You've got %s Copyleaks %s API credits" % (cloud.getCredits(), cloud.getProduct()))
    # process = cloud.createByText('Something To Worry', options)

    # iscompleted = False
    # while not iscompleted:
    #     # Get process status
    #     [iscompleted, percents] = process.isCompleted()
    #     print ('%s%s%s%%' % ('#' * int(percents / 2), "-" * (50 - int(percents / 2)), percents))
    #     if not iscompleted:
    #         time.sleep(2)

    # print ("Process Finished!")

    # # Get the scan results
    # results = process.getResults()
    # print ('\nFound %s results...' % (len(results)))
    # for result in results:
    #     print('')
    #     print('------------------------------------------------')
    #     print(result)

    # print("You've got %s Copyleaks %s API credits" % (cloud.getCredits(), cloud.getProduct()))
        

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
