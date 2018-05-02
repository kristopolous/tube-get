#!/usr/bin/python

import sys,os,re,pprint,subprocess

UA="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/41.0"
re_generic_url = re.compile('(http[:\s\/\w\.]*(?:flv|mp4)[^"\']*)')
re_kv_url = re.compile('(?<=file=)(http[:\s\/\w\.]*(?:flv|mp4)[^"\']*)')
pp = pprint.PrettyPrinter(indent=4)

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def log(what):
    print(">> %s" % what)

# If everything else failed then we look for an rtmp stanza
# which is usually supplied in JSON and using flowplayer 
def rtmpsearch(page, param):
    path = re.findall('url:\s*[\'\"](.*(?:flv|mp4))[\'\"]', page)
    base = re.findall('netConnectionUrl:\s*[\'\"](rtmp:[^\'\"]*)', page)

    if path and base:
        # for some weird reason rtmpdump has a bug where it eats up the path
        url = "%s/a/a%s" % (base[0], path[0])
        log("Found rtmp, using %s" % url)
        outfile = url.split('/')[-1]
        options = " ".join([
            '-Rr',
            shellquote(url),
            '-o',
            shellquote(outfile)
        ])

        os.popen('rtmpdump %s &' % options)
        return ['rtmp', url, param]

    return [False, False, param]

def grab(line, param=False):
    if len(line) == 0:
        return False

    source_url = line

    line = re.sub('\(', '%28', line)
    line = re.sub('\)', '%29', line)
    line = re.sub(';', '\;', line)

    domain = re.search('(http[:\s\/]*[^\/]*)', line).group(1)
    cmd = 'curl -L -e "{}" -s -A "{}" "{}"'.format(domain, UA, line)
    print(cmd)
    page = os.popen(cmd).read()
    if not param:
        param = len(page)

    #log(line)
    video = re.findall('(http[:\-\s\/\w\.]*(?:flv|mp4)\??[^"\']*)[\"\']', page)
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
        return ['get', video[0], param]

    if not video:
        iframe = re.findall('iframe[^>]*src=.(http[^"]*)', page)
        if iframe:
            log("Found iframe: %s" % iframe[0])
            return grab(iframe[0], param)
        else:
            return rtmpsearch(page, param)

    return [False, False, param]


while True:
    line = sys.stdin.readline().strip()
    """
    if os.path.exists('/usr/bin/xclip'):
        print("xclip")
        p = subprocess.Popen(['/usr/bin/xclip','-verbose'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        p.stdin.write(b'\n')
        p.communicate()[0]
        p.stdin.close()
        sys.exit(0)
    """

    if len(line) == 0:
        continue

    try:
        video = grab(line)
    except:
        print "Failed to read %s" % line
        continue

    if video[0] == False:
        url = "(FAILED)"
    else:
        url = video[1]
        if video[0] == 'get':
            has_domain = re.search('(http[:\s\/]*[^\/]*)', url) 

            if not has_domain:
                video = "%s/%s" % (domain, url)

            url = url.strip('\'"')

            options = " ".join([
                '--no-use-server-timestamps',
                '--header="Referer: %s"' % line,
                '--user-agent="{}"'.format(UA),
                shellquote(url)
            ])

            print(options)
            os.popen('wget %s &' % options)

    with open("tube-get.sources-list.txt", "a") as mylog:
        if video:
            url = video[1]
        else:
            url = 'FAILED'
            log("Failed for {} (size:{})".format(line, video[2]))

        mylog.write("%s -> %s\n" %( line, url ))

