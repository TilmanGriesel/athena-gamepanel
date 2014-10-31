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

MODULE_NAME="COD4"
SERVER_NAME=$1
USER_NAME="athena-gamepanel"
USER_GROUP="athena-gamepanel"

BASE_PATH="/opt/athena"
MODULE_PATH=$BASE_PATH"/modules/server/"$MODULE_NAME
SOURCE_PATH=$MODULE_PATH"/sources/1.7"
TARGET_PATH=$BASE_PATH"/_SERVER/"$SERVER_NAME
LOG=$BASE_PATH"/log/server/"$MODULE_NAME"_"$SERVER_NAME".log"

SERVER_MAIN="cod4_lnxded"
SERVER_ARGS="+set dedicated 2 +set fs_game mods/dirty_promod211 +set sv_punkbuster 0 +exec conf_dpm211.cfg +map_rotate"

if [ -z "$SERVER_NAME" ]
  then
    echo "No servername supplied."
    echo "Usage: ./main.sh ServerName"
    exit 1
fi

echo "--------------------------------------------"
echo "STARTING "$MODULE_NAME" SERVER ["$SERVER_NAME"]"
echo "Server:" $SERVER_MAIN
echo "Arguments:" $SERVER_ARGS
echo "Target Path:" $TARGET_PATH
echo "--------------------------------------------"

# Validate if server exsists
if [ -d "$TARGET_PATH" ]
then
    echo "Server found."
else
    echo "Server not found!"
    exit 1
fi

# Change dir to target path
cd $TARGET_PATH

# Create Logfile
echo "----------------"$(date +%s)"---------------" &>> $LOG
# Set logfile permissions
echo "Settings permissions ..."
chmod 660 $LOG
chown -R :$USER_GROUP $LOG

# Startup server
echo "Starting up gameserver ..."
su -c "./$SERVER_MAIN $SERVER_ARGS &>> $LOG" -s /bin/sh $USER_NAME
