
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

SERVERLIST_REFRESH_INTERVAL = 5000

$(function() {
    // Compile handlebar templates
    var source   = $("#server-control-template").html();
    var template = Handlebars.compile(source);

    refreshServers();

    function refreshServers() {
       setTimeout(refreshServers, SERVERLIST_REFRESH_INTERVAL);
       getServers();
    }

    // Get the server list
    function getServers() {
        console.log("Refreshing server list ...");
        var jqxhr = $.get("/api/v1/server/list", function() {})
          .done(function(data) {
            console.log(data);
            // Create data provider
            // (maybe the data could be the data provider in the future)
            var data = {servers: data};
            $("#servers").html(template(data));
            registerEventListeners();
          })
          .fail(function() {
            swal({title: "Oops...", text: "Unable to refresh the server list!", type: "error", timer: 1200});
          })
          .always(function() {
          });
        jqxhr.always(function() {});        
    }

    function registerEventListeners() {
        // Remove previous event listeners
        $("button.server-start").unbind("click");
        $("button.server-stop").unbind("click");
        
        //Register event listeners
        // Server actions
        $("button.server-start").click(function() {
            var closestServerTools = $(this).closest(".server-tools")
            var serverID = $(closestServerTools).data("serverid");
            var serverName = $(closestServerTools).data("servername");
            $.post("/api/v1/server/" + serverID + "/start", {value:serverID}, function(data) {
                if(data.type == "success") {
                    swal({title: "Server is starting", text: "Please wait a few seconds to complete!", type: "success", timer: 3500});
                    refreshServers();
                }
                else {
                    swal({title: data.message, text: "Unable to start " + serverName + " (#" + data.code + ")", type: "error"});
                }
            });
        });
        $("button.server-stop").click(function() {
            var closestServerTools = $(this).closest(".server-tools")
            var serverID = $(closestServerTools).data("serverid");
            var serverName = $(closestServerTools).data("servername");
            swal(
                {title: "Are you sure?", text: "This operation will stop the server immediately!", type: "warning", showCancelButton: true, confirmButtonColor: "#DD6B55", confirmButtonText: "Yes, stop!", closeOnConfirm: false },
                function(){
                    $.post("/api/v1/server/" + serverID + "/stop", {value:serverID}, function(data) {
                        if(data.type == "success") {
                            swal({title: "Server is stopping", text: "Please wait a few seconds to complete!", type: "success", timer: 3500});
                            refreshServers();
                        }
                        else {
                            swal({title: data.message, text: "Unable to stop " + serverName + " (#" + data.code + ")", type: "error"});
                        }
                    });
                });
        });  
    }
});