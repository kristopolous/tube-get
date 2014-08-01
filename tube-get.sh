#!/bin/bash
cd $1
while [ 0 ]; do
  read page
  video=`curl -s "$page" | grep -oP '(http[:\s\/\w\.]*mp4)[\"]' | head -1`
  if [ -z "$video" ]; then
    url=`curl -s "$page" | grep -oP '([:\/\w\.]*playerConfig.php[^"]*)' | uniq`
    echo $url
    video=`curl -s "$url" | grep defaultVideo | sed s/defaultVideo:// | sed -E s/'\;.*'// | tr '\t' ' ' | sed -E 's/\s+//'`
  fi

wget \
  --header="Referer: $page" \
  --user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0"\
  -c "$video" &
done 
