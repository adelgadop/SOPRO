#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
    
server = ECMWFDataServer(url="https://api.ecmwf.int/v1",
                         key="",
                         email="adelgado@iag.usp.br")
    
server.retrieve({
    'stream'    : "oper",
    'levtype'   : "pl",
    "levelist"  : "1/2/3/5/7/10/20/30/50/70/100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/750/775/800/825/850/875/900/925/950/975/1000",
    'param'     : "129/130/131/132/133/157",
    'dataset'   : "interim",
    'step'      : "0",
    'grid'      : "0.75/0.75",
    'time'      : "00/06/12/18",
    'date'      : "2017-09-01/to/2017-09-10",
    'type'      : "an",
    'class'     : "ei",
    'target'    : "interim_pl_2017-09-01to2017-09-10_00061218.grib"
})
