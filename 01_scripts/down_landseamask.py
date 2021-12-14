#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer(url="https://api.ecmwf.int/v1",
                         key="4c68d8ca6b594b8624233acbfb91ef31",
                         email="adelgado@iag.usp.br")
server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "1989-01-01",
    "expver": "1",
    "grid": "0.75/0.75",
    "levtype": "sfc",
    "param": "172.128",
    "step": "0",
    "stream": "oper",
    "time": "12:00:00",
    "type": "an",
    "target": "LSM:1989-01-01_12",
})
