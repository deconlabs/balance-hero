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

const message = "THIS IS A TEST MESSAGE.\n";

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
    app.get("/message", function (req, res) {
        res.send(message);
    });

    /**
     * POST example
     */
    /*
        app.post("/...", function (req, res) {
            res.send();
        });
    */
    app.post("/stop", function (req, res) {
        res.send({ "msg": "Stopping server\n" });
        process.exit();
    });

    app.listen(http_port, function () { console.log("Listening http port on: " + http_port) });
}

// main
initHttpServer();
// console.log(nw.getTable());
