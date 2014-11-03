
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.
// 
// Authors:
//     Tilman Griesel - rocketengine.io

$(function() {
    
    // Compile handlebar templates
    var source   = $("#server-control-template").html();
    var template = Handlebars.compile(source);  

    // Get the server list
    // ToDo: Error handling
    $.get("/api/v1/server/list")
        .done(function(data) {
            var servers = [];
            for(var i = 0; i < data.length; i++) {
                servers.push({ servername: data[i].info.server.name, status:"none", online: false, error: false });
            }
            var data = {servers: servers};
            $("#servers").html(template(data));
        });

    // Server actions
    $( "#action" ).click(function() {
        $.post("/api/v1/server/COD4DIRTY/start", {value:"none"}, function(data) {
           alert(data.value);
        });
    });
});