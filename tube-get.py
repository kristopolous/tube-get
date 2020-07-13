#!/usr/bin/python3
import datetime
import time
import logging
import sys,os,re,pprint,subprocess

UA="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/41.0"
re_generic_url = re.compile('(http[:\s\/\w\.]*(?:flv|mp4)[^"\']*)')
re_kv_url = re.compile('(?<=file=)(http[:\s\/\w\.]*(?:flv|mp4)[^"\']*)')
pp = pprint.PrettyPrinter(indent=4)
oneurl = False
start = time.time()

if len(sys.argv) > 1:
    if os.path.isdir(sys.argv[1]):
        os.chdir(sys.argv[1])
    else:
        oneurl = sys.argv[1]

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
    else:
        log("No rtmp found")

    return [False, False, param]

def probe(html, param=False, depth=1, onlyurl=False):
    maxlevel=5
    if depth > maxlevel:
        log("{} levels deep, giving up".format(maxlevel))
        return [False, False, False]

    #log(line)
    video = re.findall('(http[:\-\s\/\w%\.=,+]*(?:flv|mp4)\??[^"\']*)[\"\']', html)
    if video:
        video = filter(lambda x: x.find('.jpg') == -1, video)
        video = filter(lambda x: x.find('/thumbs/') == -1, video)
        if not onlyurl:
            print(video)

    if not video:
        log("No mp4 found")
        player_config_url = re.findall('([:\/\w\.]*playerConfig.php[^"]*)', html)

        if not player_config_url:
            log("No config php found")
            video = re_kv_url.findall(html)
            #print video

            if not video:
                video = re_generic_url.findall(html)
                #print video

        else:
            #print player_config_url
            video = re_kv_url.search(html)
            if not video:
                video = re_generic_url.findall(html)

        #print player_config_url

    video = list(filter(lambda x: x.find('preview') == -1, video))
    #pp.pprint(video)

    if video:
        return ['get', video[0], param]

    if not video:
        iframe = re.findall('iframe[^>]*src=.(http[^"]*)', html)
        if iframe:
            log("Found iframe: %s" % iframe[0])
            res = grab(iframe[0], param, depth+1)
        else:
            log("No iframe found")
            res = rtmpsearch(html, param)

    if res[0] == False:
        jsSnippet = re.findall('<script>(.+?(?=</script>))', html.replace('\n',' '), re.MULTILINE)
        if jsSnippet:
            candidateList = filter(lambda x: x.find('String.fromCharCode') > -1, jsSnippet)
            if len(candidateList) > 0:
                attempt = candidateList[0]
                if attempt.find('document.write') > -1:
                    attempt = attempt.replace('document.write', 'console.log')

                    cmd = "/usr/local/bin/node -e {}".format(shellquote(attempt))
                    snippet = os.popen("/usr/local/bin/node -e {}".format(shellquote(attempt))).read()
                    log("Found javascript obfuscation: {}".format(snippet))

                    res = probe(snippet, param, depth+1)
        if res[0] == False:
            log("No obfuscated JS found")

    return res

def grab(line, param=False, depth=1, onlyurl=False):
    if len(line) == 0:
        return False

    source_url = line

    line = re.sub('\(', '%28', line)
    line = re.sub('\)', '%29', line)
    line = re.sub(';', '\;', line)

    domain = re.search('(http[:\s\/]*[^\/]*)', line)
    if domain:
        domain = domain.group(1)
        cmd = 'curl --tcp-fastopen -4 -L -e {} -s -A {} {}'.format(shellquote(domain), shellquote(UA), shellquote(line))
        if not onlyurl:
            print(cmd)
        page = os.popen(cmd).read()
        if not param:
            param = len(page)
    elif os.path.isfile(line):
        with open(line) as f:
            page = f.read()

    return probe(page, param, depth, onlyurl=onlyurl)

while True:
    if oneurl:
        line = oneurl
    else:
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

    #try:
    video = grab(line, onlyurl=oneurl)

    if oneurl:
        if video:
            print(video[1])
        sys.exit(0)
    #except:
    #    print "Failed to read %s" % line
    #   continue

    if video[0] == False:
        url = "(FAILED)"
    else:
        url = video[1]
        if video[0] == 'get':
            has_domain = re.search('(http[:\s\/]*[^\/]*)', url) 

            if not has_domain:
                video = "%s/%s" % (domain, url)

            url = url.strip('\'"')
            fname = re.sub('\?.*', '', url).rstrip('/').split('/')[-1]

            options = " ".join([
                '-O {}'.format(shellquote(fname)),
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

        mylog.write("%s %s -> %s\n" %( datetime.datetime.utcnow(), line, video[1] ))


