# tube-get

There's a bunch of adult content video sites out there. This is a browser independent easy way to download their content for free.

The business models are fairly similar: You watch an allotment of videos in their embedded player per some time period and then you have to pay.

They seem to be using mostly the same software to do this. It's pretty trivial to work around since it leaks enough information for you to derive the location of the content before it presents you with the paywall.

I've had a number of solutions over the years, but the latest I'm proud of for its simplicity.

# Usage

Written in bash, it takes URLs from the standard in.  You execute and then put URLs in the input

    $ ./tube-get.sh [ Directory to save stuff ]
    http://somevideosite.com/somevideolink.html

These correspond to the links if you were to click through to the page with their embedded player. (as in, right click in the browser, copy link to clipboard, then paste it into the terminal)

After you press enter the magic begins.  The script runs a few attempts trying to sniff the common pre-packaged technologies that are used to build these sites and derives the video url.

Then it will download the content and save it locally.

## Runs in the background.

It's important to note that when it's wget'ing the content, it's in the background.  The script is ready at this time for more urls.

You don't have to wait.  Just paste another in there and it will do the magic and spawn another wget.  

## Conclusion

So this is a pretty slick method - it doesn't use cookies or run in the browser at all so you don't get punted the paywall.  Further, it's generic enough that it works on a large variety of sites without actually having to specify the site or do the up-keep - previous soultions I had would use elements from the generated page to concoct a url. 

I found that none of this was actually necessary - either a direct link to the video or a link to a "flash vars" file which has the video exists in the html of 95% of the sites I've tried.

So that's it -- a few curls, a few greps --- that's all that you need.

### Isn't this unethical

Essentially 100% of the content on these sites were uploaded without the permission of the creator.  They are charging you to view content that they have no legal right to distribute or show - yet alone profit from.

So fuck 'em. Also, the embedded video players are terrible. They don't buffer right, the scrubbing is awful, the offsetting is inaccurate, the decoding is really poor ... I mean it's across the board a terrible experience.

## Support

If you'd like it to work on a site that it's not, file an issue and I'll see if it's an easy fix.  Thanks.
