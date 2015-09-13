#!/usr/bin/python

import sys,os,re

re_generic_url = re.compile('(http[:\s\/\w\.]*(flv|mp4))')
re_kv_url = re.compile('(?<=file=)(http[:\s\/\w\.]*(flv|mp4))')

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

while True:
    line = sys.stdin.readline()
    domain = re.search('(http[:\s\/]*[^\/]*)', line).group(1)
    page = os.popen('curl -s %s' % line).read()

    video = re.search('(http[:\s\/\w\.]*(flv|mp4))[\"]', page)
    if not video:
        player_config_url = re.search('([:\/\w\.]*playerConfig.php[^"]*)', page)

        if not player_config_url:
            video = re_kv_url.search(page)
            print video

            if not video:
                video = re_generic_url.search(page)
                print video

        else:

            video = re_kv_url.search(page)
            if not video 

        print player_config_url


    print video
