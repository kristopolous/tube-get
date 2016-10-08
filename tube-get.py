#!/usr/bin/python

import sys,os,re,pprint

re_generic_url = re.compile('(http[:\s\/\w\.]*(?:flv|mp4))')
re_kv_url = re.compile('(?<=file=)(http[:\s\/\w\.]*(?:flv|mp4))')
pp = pprint.PrettyPrinter(indent=4)

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def log(what):
    print(">> %s" % what)

def grab(line):
    if len(line) == 0:
        return False

    source_url = line

    line = re.sub('\(', '%28', line)
    line = re.sub('\)', '%29', line)
    line = re.sub(';', '\;', line)

    domain = re.search('(http[:\s\/]*[^\/]*)', line).group(1)
    page = os.popen('curl -s %s' % line).read()
    #log(line)
    video = re.findall('(http[:\-\s\/\w\.]*(?:flv|mp4))[\"\'\&]', page)
    if not video:
        log("No mp4 found")
        player_config_url = re.findall('([:\/\w\.]*playerConfig.php[^"]*)', page)

        if not player_config_url:
            log("No config php found")
            video = re_kv_url.findall(page)
            #print video

            if not video:
                video = re_generic_url.findall(page)
                #print video

        else:
            #print player_config_url
            video = re_kv_url.search(page)
            if not video:
                video = re_generic_url.findall(page)

        #print player_config_url

    video = filter(lambda x: x.find('preview') == -1, video)
    #pp.pprint(video)

    if video:
        return video[0]

    if not video:
        iframe = re.findall('iframe src=.(http[^"]*)', page)
        if iframe:
            log("Found iframe")
            return grab(iframe[0])


while True:
    line = sys.stdin.readline().strip()
    video = grab(line)

    if not video:
        continue

    has_domain = re.search('(http[:\s\/]*[^\/]*)', video) 

    if not has_domain:
        video = "%s/%s" % (domain, video)

    video = video.strip('\'"')

    print video
    options = " ".join([
        '--no-use-server-timestamps',
        '--header="Referer: %s"' % source_url,
        '--user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/41.0"',
        shellquote(video)
    ])

    os.popen('wget %s &' % options)

    with open("tube-get.sources-list.txt", "a") as log:
        log.write("%s -> %s\n" %( source_url, video ))

