#bin/sh

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
SERVER_VERSION="1.7"
USER_GROUP="athena-gamepanel"

BASE_PATH="/opt/athena-gamepanel"
MODULE_PATH=$BASE_PATH"/modules/server/"$MODULE_NAME
SOURCE_PATH=$MODULE_PATH"/sources/"$SERVER_VERSION
TARGET_PATH=$BASE_PATH"/_SERVER/"$SERVER_NAME

if [ -z "$SERVER_NAME" ]
  then
    echo "No servername supplied."
    echo "Usage: ./"$SERVER_VERSION".sh ServerName" 
    exit 1
fi

# Validate if server does not already exsists
if [ -d "$TARGET_PATH" ]
then
    echo "Server already exsists!"
    exit 1
fi

echo "Creating new "$MODULE_NAME" ("$SERVER_VERSION") Server ..."

# Create folder structure
mkdir $TARGET_PATH

# Change dir to target path
cd $TARGET_PATH

# Link root files
rootFiles=( README.linux cod4_lnxded cod4_lnxded-bin libgcc_s.so.1 libstdc++.so.6 pbsetup.run zone )
for i in "${rootFiles[@]}"
do
	ln -s  $SOURCE_PATH/$i
done

# Link main files
mkdir main
ln -s $SOURCE_PATH/main/* main/

mkdir main/usermaps
mkdir main/mods

# Set permissions
echo "Setting permissions ..."
chown -R :$USER_GROUP $MODULE_PATH
chmod -R 750 $MODULE_PATH
chown -R :$USER_GROUP main
chmod -R 750 main

echo "Done. Created Server: "$MODULE_NAME
