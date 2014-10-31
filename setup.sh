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

LOG="log/setup/setup.log"
USER_NAME="athena-gamepanel"
USER_PASS=$(openssl rand -base64 16)
USER_GROUP="athena-gamepanel"

# Make sure only root can run this script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "--------------------------------------------"
echo "ATHENA SETUP STARTED"
echo "--------------------------------------------"

echo "Creating folder structure ..."
mkdir -p log
mkdir -p log/setup
mkdir -p log/server
mkdir -p _SERVER &>> $LOG
mkdir -p modules &>> $LOG

echo "Clean up ..."
skill -KILL -u $USER_NAME &>> $LOG # Kill user session
userdel $USER_NAME &>> $LOG # Delete user

echo "Creating user ..."
groupadd $USER_GROUP
useradd -m -p $USER_PASS $USER_NAME -g $USER_GROUP &>> $LOG # Add user to the system

echo "Setting permissions ..."
chown -R :$USER_GROUP _SERVER/ &>> $LOG
chown -R :$USER_GROUP log/ &>> $LOG

chmod -R 770 log &>> $LOG
chmod -R 770 _SERVER &>> $LOG
chmod 700 setup.sh &>> $LOG

echo "--------------------------------------------"
echo "ATHENA SETUP COMPLETED"
echo "Username:" $USER_NAME
echo "Password:" $USER_PASS
echo "--------------------------------------------"
exit 0
