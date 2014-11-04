#!/bin/sh

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

# ------------------------------
# Environment
# ------------------------------

USER_NAME="athena-gamepanel"
USER_GROUP="athena-gamepanel"
BASE_PATH="/opt/athena-gamepanel"
SERVER_PATH=$BASE_PATH"/_SERVER"
MODULE_PATH=$BASE_PATH"/modules/server"
LOG_PATH=$BASE_PATH"/log"
WEB_PATH=$BASE_PATH"/web"

# ------------------------------
# Welcome message
# ------------------------------

echo "--------------------------------------------"
echo "STARTING ATHENA WEBSERVICE"
echo "--------------------------------------------"

# ------------------------------
# Cleanup leftovers
# ------------------------------

echo "Killing all "$USER_NAME" processes ..."
pkill -u $USER_NAME

# ------------------------------
# Ensure Permissions
# ------------------------------

echo "Ensuring permissions ..."
# Module permissions
chown -R :$USER_GROUP $SERVER_PATH
chmod -R 750 $SERVER_PATH
# Server permissions
chown -R :$USER_GROUP $SERVER_PATH
chmod -R 750 $SERVER_PATH
# Log permissions
chown -R :$USER_GROUP $LOG_PATH
chmod -R 770 $LOG_PATH
# Web permissions
chown -R :$USER_GROUP $WEB_PATH
chmod -R 770 $WEB_PATH

# ------------------------------
# Web App
# ------------------------------

echo "Starting web app ..."
su -c "python app.py" -s /bin/sh $USER_NAME