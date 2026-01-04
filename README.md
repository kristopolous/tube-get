## tube-get

**tube-get** is a python script that acts as a browser independent easy way to freely download video content from video sites.

You use `yt-dlp`? Good! Me too. 

Doesn't always work. When it doesn't, tube-get is the more blunt hammer.

# Usage

There's an interactive (REPL) and non-interactive mode.

## Interactive

Start `tube-get` by specifying a directory to save videos to and then paste URLs in the console after you start:

    $ ./tube-get.py [ Directory to save stuff ]
    http://somevideosite.com/somevideolink.html

These correspond to the links if you were to click through to the page with their embedded player. (as in, right click in the browser, copy link to clipboard, then paste it into the terminal)

After you press enter the magic begins.  The script runs a few attempts trying to sniff the common pre-packaged technologies that are used to build these sites and derives the video url.

Then it will download the content and save it locally. It doesn't use the `<title>` from the site, which is often just a bunch of NSFW words smacked together. A directory full of files with names like 5a96131c58ef9.mp4 is probably ok.  I should probably make a separate sqlite way to organize them though.

Some features:
 
 * Looks for embed tags and can follow them
 * Knows how to deal with rtmp streams (you need rtmpdump for it).
 * Figures what the proper HTTP referer to use is
 * Logs the timestamp, link that it started with, and what it was derived to ... or if it was a failure

### Runs in the background.

When it's wget'ing the content the script is ready at this time for more urls.

You don't have to wait.  Just paste another in there and it will do the magic and spawn another wget.  

## Non-interactive mode

If the argument contains `http`, then `tube-get` treats the argument as a URL and outputs the final mp4/flv link and exits.  In practice, this can operate like the `ytdl` option in mpv since it translates a URL to its corresponding direct mp4.

Essentially you can do

```
tp() { 
  mpv $(tube-get.py $1)
}
```

then just do:

    $ tp <url>

on the command line. Super fast. 

You can also use the other UX pattern by doing a 1-line REPL like this:

    $ while read url; do mpv $(tube-get.py $url)&; done

## Even faster ways

The tool "clipwatch" in here will watch your clipboard and then optionally run a command if it changes.

So if you do something like

    $ echo "tp() { mpv $(tube-get.py $1) } > tp
    $ chmod +x tp
    $ bin/clipwatch tp

And then rightclick, copy link. It will feed it into the tp command while clipwatch is running. Pretty sw33t

## Conclusion

This method doesn't use cookies or run in the browser at all so you leave as light of a footstep as you can.  Further, it's generic enough that it works on a large variety of sites without actually having to specify the site or do the up-keep - previous solutions I had would use elements from the generated page to concoct a url. 

I found that none of this was actually necessary - either a direct link to the video or a link to a "flash vars" file which has the video exists in the html of 95% of the sites I've tried. When a site breaks this I generally spend some time to fix it.  So I keep it pretty up to date.

## Support

If you'd like it to work on a site that it's not, file an issue and I'll see if it's an easy fix. If you want to do it anonymously, totally understood although there's no place I'd be checking for anonymous tickets. I have another project that is meant to address this and this will be my first test case
