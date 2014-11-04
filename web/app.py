# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# 
# Authors:
#     Tilman Griesel - rocketengine.io

# ---------------------------------------------------
# Athena Web Interface
# ---------------------------------------------------

# ---------------------------------------------------
# Imports
# ---------------------------------------------------

import os, random, string
import uuid
from flask import Flask, render_template, redirect, g, request, url_for, abort
from flask.ext.httpauth import HTTPDigestAuth
from flask.ext.restful import Resource, Api, reqparse
from subprocess import Popen, PIPE, STDOUT
import psutil
import signal
import json
import time
import shelve

# ---------------------------------------------------
# Secret Helpers
# ---------------------------------------------------

def getSecret(length):
    chars = string.ascii_letters + string.digits
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(chars) for i in range(length))

# ---------------------------------------------------
# Settings
# ---------------------------------------------------

app = Flask(__name__)
auth = HTTPDigestAuth()
api = Api(app)

db = shelve.open('db')

# Get keys
if not db.has_key("ROOT_KEY"): db['ROOT_KEY'] = getSecret(32)
if not db.has_key("SECRET_KEY"): db['SECRET_KEY'] = getSecret(32)
app.config['ROOT_KEY'] = db['ROOT_KEY']
app.config['SECRET_KEY'] = db['SECRET_KEY']

rootPath = "/opt/athena-gamepanel"
users = { "root": app.config['ROOT_KEY']}
active_servers = {}

# ---------------------------------------------------
# Authentication
# ---------------------------------------------------

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# ---------------------------------------------------
# Process helper
# ---------------------------------------------------

def launchProcess(command, workingdir, logfile):
    owd = os.getcwd()
    os.chdir(workingdir)
    procMain = Popen(command, shell=False, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
    procLog = Popen(['tee', logfile], stdin=procMain.stdout, stdout=PIPE)
    os.chdir(owd)
    return [procMain, procLog]

def checkPid(pid):        
    try: os.kill(pid, 0)
    except OSError: return False
    else: return True

# ---------------------------------------------------
# Server Start
# ---------------------------------------------------

def startServerById(id):
    if id in active_servers:
        return {'type':'error', 'message': 'Server is already started!', 'code': 4010}

    # Query server info
    serverRootPath = rootPath + '/_SERVER'
    try: serverInfoFile = open(serverRootPath + '/' + id + '/info.json', 'r')
    except IOError: return {'type':'error', 'message': 'Server not found', 'code': 4011}
    try: serverInfo = json.loads(serverInfoFile.read())
    except TypeError: return {'type':'error', 'message': 'Unable to read server info', 'code': 4012}
    
    # Query module info
    moduleRootPath = '../modules/server'
    try: moduleInfoFile = open(moduleRootPath + '/' + serverInfo['module']['name'] + '/module.json', 'r')
    except IOError: return {'type':'error', 'message': 'Module not found', 'code': 4013}
    try: moduleInfo = json.loads(moduleInfoFile.read())
    except TypeError: return {'type':'error', 'message': 'Unable to read module info', 'code': 4014}

    # Launch server
    logfile = rootPath + '/log/server/' + id + '.log'
    mainPath = serverRootPath + '/' + id
    main = ['./' + moduleInfo['main']]
    args = ['+set dedicated 2', '+set fs_game mods/dirty_promod211', '+set sv_punkbuster 0', '+exec conf_dpm211.cfg', '+set rcon_password "mypass"', '+map_rotate']
    try:
        active_servers[id] = launchProcess(main + args, mainPath, logfile)
        print "Starting server:" + serverInfo['server']['name']
        return {'type':'success', 'message': 'Server started!', 'code': 2010}
    except:
        print "Unable to start server!"
        return {'type':'error', 'message': 'Unable to start server!', 'code': 4015}

def stopServerById(id):
    if id in active_servers:
        print "Stopping server by ID: " + id
        try:
            for proc in active_servers[id]:
                print checkPid(proc.pid)
                if checkPid(proc.pid) is True:
                    os.kill(proc.pid, signal.SIGKILL)
                    proc.wait()
            active_servers.pop(id, None)
            return {'type':'success', 'message': 'Server stopped!', 'code': 2020}
        except:
            return {'type':'error', 'message': 'Unable to stop server!', 'code': 4025}
    else:
        return {'type':'error', 'message': 'Server is not started!', 'code': 4020}

# ---------------------------------------------------
# App Routing
# ---------------------------------------------------

@app.route('/')
@auth.login_required
def root():
    return render_template('index.html')

launchServerArgs = reqparse.RequestParser()
launchServerArgs.add_argument('name', type=str)

class StartServer(Resource):
    @auth.login_required
    def post(value, id):
        args = launchServerArgs.parse_args()
        response = startServerById(id)
        return response

class StopServer(Resource):
    @auth.login_required
    def post(value, id):
        args = launchServerArgs.parse_args()
        response = stopServerById(id)
        return response

class GetServers(Resource):
    @auth.login_required
    def get(value):
        response = []
        rootdir = rootPath + '/_SERVER'
        for serverid in os.listdir(rootdir):
            if os.path.isfile(serverid): pass
            else:
                infoPath = open(rootdir + '/' + serverid + '/info.json', 'r')
                # Get info json (generated by the recipes)
                try: info = json.loads(infoPath.read())
                except IOError: pass
                # Get active state
                active = False
                if serverid in active_servers : active = True
                # Build up server entry
                server = {'id': serverid, 'active': active, 'info': info}
                # Append to server list
                response.append(server)
        return response

api.add_resource(StartServer, '/api/v1/server/<string:id>/start')
api.add_resource(StopServer, '/api/v1/server/<string:id>/stop')
api.add_resource(GetServers, '/api/v1/server/list')

# ---------------------------------------------------
# Init
# ---------------------------------------------------

if __name__ == '__main__':
    # Print startup messages
    print "SECRET KEY: " + app.config['SECRET_KEY']
    print "ROOT KEY: " + app.config['ROOT_KEY']
    # Init app
    app.run(host='0.0.0.0', port=2020, debug=True)





