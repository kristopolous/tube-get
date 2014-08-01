# tube-get

There's a bunch of adult content video sites out there.

Their business models are fairly similar: You can watch an alotment of videos in their embedded player per some time period, and then you have to pay.

They seem to probably be mostly using the same software to do this. It's pretty trivial to work around since they almost always leak enough information for you to derive the location of the content before presenting you with the paywall.

I've had a number of solutions over the years, but the latest I'm proud of for its simplicity.

# usage

It's written in bash and takes URLs from the standard in.  You execute and then put URLs in the input

    $ ./tube-get
    http://somevideosite.com/somevideolink.html

These correspond to the links that the tube sites have --- if you were to click through to the page with their embedded player.

After you press enter, then the magic begins.  It runs a few attempts trying to sniff the common pre-packaged technologies that are used to build these sites and tries to derive the video url.

Then it will download the content and save it locally.

## Runs in the background.

It's important to note that when it's wget'ing the content, it's in the background.  The script is ready at this time for more urls.

You don't have to wait.  Just paste another in there and it will do the magic and spawn another wget.  

Run 20 ... it doesn't matter.

## Conclusion

So this is a pretty slick method - it doesn't use cookies so you don't get punted the paywall and it's generic enough that it works on a large variety of sites without actually having to specify the site or do the up-keep.

If you'd like it to work on a site that it's not, file an issue and I'll see if it's an easy fix.  Thanks.
