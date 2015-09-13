#!/usr/bin/python

import sys,os,fileinput

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

for line in fileinput.input():
    pass
