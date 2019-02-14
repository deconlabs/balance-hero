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
var t;  // setTimeout()

var orders = [];  // [{"id": 0, "when": 90, "amount": 10}, ...]

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
            res.send({
                "msg": "MUST SET STACK FIRST.\n"
            });
        }
        else {
            res.send({
                "stack": stack
            });
        }
    });

    app.get("/timer", function (req, res) {
        if (timer == -1) {
            res.send({
                "msg": "MUST SET TIMER FIRST.\n"
            });
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

    app.get("/orderBook", function (req, res) {
        res.send({
            "orderBook": orders
        });
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
        
        res.send({
            "msg": "SUCESSFULLY SET STACK.\n"
        });
    });

    app.post("/setTimer", function (req, res) {
        timer = req.body.timer;
        startTime = getCurrentTimestamp();

        t = setTimeout(function () {
            console.log("Stopping server\n");
            // process.exit();
            timer = -1;
            startTime = -1;
        }, timer);

        res.send({
            "msg": "SUCESSFULLY SET TIMER.\n"
        });
    });

    app.post("/purchase", function (req, res) {
        if (timer == -1) { res.send({ "msg": "MUST SET TIMER FIRST.\n" });}
        else {
            var amount = req.body.amount;
            if (amount <= 0 || stack - amount < 0) { res.send({ "msg": "INVALID AMOUNT.\n" }); }
            else {
                var agentId = req.body.id;
                if (agentId == undefined) { res.send({ "msg": "INVALID ID.\n" }); }
                else {
                    orders.push({
                        "id": agentId,
                        "when": stack,
                        "amount": amount
                    });

                    stack -= amount;

                    res.send({
                        "msg": "SUCESSFULLY PURCHASE.\n"
                    });
                }
            }
        }
    });

    app.post("/reset", function (req, res) {
        stack = -1;

        clearTimeout(t);
        timer = -1;
        startTime = -1;

        res.send({
            "msg": "SUCCESSFULLY RESET.\n"
        });
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
