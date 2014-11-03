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
import json
import time
import shelve

# ---------------------------------------------------
# Helpers
# ---------------------------------------------------

def getSecret(length):
    chars = string.ascii_letters + string.digits
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(chars) for i in range(length))

# ---------------------------------------------------
# Pre-startup
# ---------------------------------------------------

# ---------------------------------------------------
# Settings
# ---------------------------------------------------

app = Flask(__name__)
auth = HTTPDigestAuth()
api = Api(app)

sdb = shelve.open('sdb')

# Get keys
if not sdb.has_key("ROOT_KEY"): sdb['ROOT_KEY'] = getSecret(32)
if not sdb.has_key("SECRET_KEY"): sdb['SECRET_KEY'] = getSecret(32)
app.config['ROOT_KEY'] = sdb['ROOT_KEY']
app.config['SECRET_KEY'] = sdb['SECRET_KEY']

users = { "root": app.config['ROOT_KEY']}

# ---------------------------------------------------
# Authentication
# ---------------------------------------------------

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# ---------------------------------------------------
# App Routing
# ---------------------------------------------------

@app.route('/')
@auth.login_required
def root():
    return render_template('index.html')

launchServerArgs = reqparse.RequestParser()
launchServerArgs.add_argument('value', type=str)

class StartServer(Resource):
    @auth.login_required
    def get(value, name):
        return name
    @auth.login_required
    def post(value, name):
        args = launchServerArgs.parse_args()
        #WriteConfig(8, args['value'])
        return args

class GetServers(Resource):
    @auth.login_required
    def get(value):
        response = []
        rootdir = '../_SERVER'
        for name in os.listdir(rootdir):
            if os.path.isfile(name): pass
            else:
                infoPath = open(rootdir + '/' + name + '/info.json', 'r')
                try: info = json.loads(infoPath.read())
                except IOError: pass
                server = {'id': name, 'info': info}
                response.append(server)
        return response

api.add_resource(StartServer, '/api/v1/server/<string:name>/start')
api.add_resource(GetServers, '/api/v1/server/list')

# ---------------------------------------------------
# Init
# ---------------------------------------------------

if __name__ == '__main__':

    # Print startup messages
    print "SECRET KEY: " + app.config['SECRET_KEY']
    print "ROOT KEY: " + app.config['ROOT_KEY']

    # Init app
    app.run(host='0.0.0.0', debug=True)





