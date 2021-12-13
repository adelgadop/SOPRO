#!/usr/bin/env python
#################################################################
# Python Script to retrieve 488 online Data files of 'ds627.0',
# total 6.14G. This script uses 'requests' to download data.
#
# Highlight this script by Select All, Copy and Paste it into a file;
# make the file executable and run it on command line.
#
# You need pass in your password as a parameter to execute
# this script; or you can set an environment variable RDAPSWD
# if your Operating System supports it.
#
# Contact davestep@ucar.edu (Dave Stepaniak) for further assistance.
#################################################################


import sys, os
import requests

def check_file_status(filepath, filesize):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

# Try to get password
if len(sys.argv) < 2 and not 'RDAPSWD' in os.environ:
    try:
        import getpass
        input = getpass.getpass
    except:
        try:
            input = raw_input
        except:
            pass
    pswd = input('Password: ')
else:
    try:
        pswd = sys.argv[1]
    except:
        pswd = os.environ['RDAPSWD']

url = 'https://rda.ucar.edu/cgi-bin/login'
values = {'email' : 'adelgado@iag.usp.br', 'passwd' : pswd, 'action' : 'login'}
# Authenticate
ret = requests.post(url,data=values)
if ret.status_code != 200:
    print('Bad Authentication')
    print(ret.text)
    exit(1)
dspath = 'https://rda.ucar.edu/data/ds627.0/'
filelist = [
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090100',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090106',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090112',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090118',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090200',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090206',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090212',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090218',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090300',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090306',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090312',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090318',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090400',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090406',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090412',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090418',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090500',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090506',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090512',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090518',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090600',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090606',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090612',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090618',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090700',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090706',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090712',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090718',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090800',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090806',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090812',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090818',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090900',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090906',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090912',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017090918',
'ei.oper.an.sfc/201709/ei.oper.an.sfc.regn128sc.2017091000']
for file in filelist:
    filename=dspath+file
    file_base = os.path.basename(file)
    print('Downloading',file_base)
    req = requests.get(filename, cookies = ret.cookies, allow_redirects=True, stream=True)
    filesize = int(req.headers['Content-length'])
    with open(file_base, 'wb') as outfile:
        chunk_size=1048576
        for chunk in req.iter_content(chunk_size=chunk_size):
            outfile.write(chunk)
            if chunk_size < filesize:
                check_file_status(file_base, filesize)
    check_file_status(file_base, filesize)
    print()
