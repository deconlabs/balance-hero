"use strict";
const WebSocket = require("ws");
const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");

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

var timer = -1; // milli-secs
var startTime = -1;
var t; // setTimeout()

var orders = []; // [{"id": 0, "when": 90, "amount": 10, "timestamp": 1589311230}, ...]

var isAlive = false;
var isSuccess = false;

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

    app.get("/status", function (req, res) {
        res.send({
            "isAlive": isAlive,
            "isSuccess": isSuccess
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

        if (timer != -1) { isAlive = true; }

        res.send({
            "msg": "SUCCESSFULLY SET STACK.\n"
        });
    });

    app.post("/setTimer", function (req, res) {
        timer = req.body.timer;
        startTime = getCurrentTimestamp();

        if (stack != -1) { isAlive = true; }

        t = setTimeout(function () {
            console.log("Stopping server\n");
            // process.exit();
            timer = -1;
            startTime = -1;
            isAlive = false;

            if (stack == 0) { isSuccess = true; }
        }, timer);

        res.send({
            "msg": "SUCCESSFULLY SET TIMER.\n"
        });
    });

    app.post("/purchase", function (req, res) {
        if (timer == -1) { res.send({ "msg": "MUST SET TIMER FIRST.\n" }); }
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
                        "amount": amount,
                        "timestamp": getCurrentTimestamp()
                    });

                    console.log(`${agentId} purchased ${amount} at ${stack}`);
                    stack -= amount;

                    if (stack == 0 && timer != -1) {
                        isAlive = false;
                        isSuccess = true;
                    }

                    res.send({
                        "msg": "SUCCESSFULLY PURCHASE.\n"
                    });
                }
            }
        }
    });

    // TODO: Reset할 때마다 json 파일에 저장하니까 file I/O에 걸리는 시간이 너무 큼
    // 내부적으로 기록을 하고 있다가 적절한 간격마다 저장을 하게 하는게 좋을 듯함
    app.post("/reset", function (req, res) {
        // write log file
        if (!fs.existsSync("../logs/")) { fs.mkdirSync("../logs/"); }

        var dealTime = 0;
        if (orders.length != 0) {
            dealTime = orders[orders.length - 1]["timestamp"] - orders[0]["timestamp"]
        }

        fs.writeFileSync("../logs/" + getCurrentTimestamp().toString() + ".json",
            JSON.stringify({
                "dealSuccess": isSuccess,
                "dealTime": dealTime,
                "orders": orders
            }),
            "utf-8")
        console.log("SYNC WRITE COMPLETE.\n");

        // reset stack
        stack = -1;

        // reset timer
        clearTimeout(t);
        timer = -1;
        startTime = -1;

        // reset orderbook
        orders = [];

        // reset flag
        isAlive = false;
        isSuccess = false;

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
