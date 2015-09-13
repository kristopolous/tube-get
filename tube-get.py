#!/usr/bin/python

import sys,os,re

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

while True:
    line = sys.stdin.readline()
    domain = re.search('(http[:\s\/]*[^\/]*)', line).group(1)
    print domain
