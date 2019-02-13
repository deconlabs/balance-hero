"use strict";
const WebSocket = require("ws");
const express = require("express");
const bodyParser = require("body-parser");

// set environment variable
const http_port = process.env.HTTP_PORT || 3000;

// network delay table
/*
    var table = setTable()
    function getTable() { return table; }
    function setTable() {
        const fs = require("fs");

        const packageJson = fs.readFileSync("./table.json");
        const table = JSON.parse(packageJson);
        return table;
    }
*/

var stack = -1;
var timer = -1;  // milli-secs
var startTime = -1;

function initHttpServer() {
    const app = express();
    app.use(bodyParser.json());

    /**
     * GET example
     */
    /*
        app.get("/...", function (req, res) {
            res.send();
        });
    */
    app.get("/stack", function (req, res) {
        if (stack == -1) {
            res.send("MUST SET STACK FIRST.\n");
        }
        else {
            res.send({
                "stack": stack
            });
        }
    });

    app.get("/timer", function (req, res) {
        if (timer == -1) {
            res.send("MUST SET TIMER FIRST.\n");
        }
        else {
            var remain = timer - (getCurrentTimestamp() - startTime);

            res.send({
                "timer": timer,
                "start": startTime,
                "remain": remain
            });
        }
    });

    /**
     * POST example
     */
    /*
        app.post("/...", function (req, res) {
            res.send();
        });
    */
    app.post("/setStack", function (req, res) {
        stack = req.body.stack;
        
        res.send();
    });

    app.post("/setTimer", function (req, res) {
        timer = req.body.timer;
        startTime = getCurrentTimestamp();

        setTimeout(function () {
            console.log("Stopping server\n");
            process.exit();
        }, timer);

        res.send();
    });

    app.post("/stop", function (req, res) {
        res.send({
            "msg": "Stopping server"
        });
        process.exit();
    });

    app.listen(http_port, function () { console.log("Listening http port on: " + http_port) });
}

function getCurrentTimestamp() {
    return new Date().getTime();
}

// main
initHttpServer();
// console.log(nw.getTable());
