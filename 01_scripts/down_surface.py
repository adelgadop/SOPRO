#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
    
server = ECMWFDataServer(url="https://api.ecmwf.int/v1",
                         key="4c68d8ca6b594b8624233acbfb91ef31",
                         email="adelgado@iag.usp.br")
    
server.retrieve({
    'stream'    : "oper",
    'levtype'   : "sfc",
    'param'     : "165/166/167/168/134/151/235/31/34/33/141/139/170/183/236/39/40/41/42",
    'dataset'   : "interim",
    'step'      : "0",
    'grid'      : "0.75/0.75",
    'time'      : "00/06/12/18",
    'date'      : "2017-09-01/to/2017-09-10",
    'type'      : "an",
    'class'     : "ei",
    'target'    : "interim_2017-09-01to2017-09-10_00061218.grib"
})
