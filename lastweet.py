#!/usr/bin/env python

# put this in your crontab to run every week if you want to tweet what your
# top 3 artists of the week are on LastFM
#
# you'll need to have tweepy and requests installed and the various keys set
# in your cron environment. Or you could set them explicitly in here if you 
# want

import os
import sys
import json
import time
import shutil
import tweepy
import mastodon
import urllib.request

from requests_html import HTMLSession

http = HTMLSession()

debug = False

# get some environment variables
e = os.environ.get
twitter_consumer_key = e('TWITTER_CONSUMER_KEY')
twitter_consumer_secret = e('TWITTER_CONSUMER_SECRET')
twitter_access_token = e('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = e('TWITTER_ACCESS_TOKEN_SECRET')
lastfm_api_key = e('LASTFM_KEY')
lastfm_user = e('LASTFM_USER')
mastodon_url = e('MASTODON_URL')
mastodon_client_id = e('MASTODON_CLIENT_ID')
mastodon_client_secret = e('MASTODON_CLIENT_SECRET')
mastodon_access_token = e('MASTODON_ACCESS_TOKEN')

# will try to download an image for a given musicbrainz artist id
def get_image(artist_url):
    doc = http.get(artist_url)
    image_url = doc.html.find('.header .avatar', first=True)
    if not image_url:
        return
    image_url = image_url.attrs['src']
    filename = os.path.join(".", "images", os.path.basename(image_url))
    r = http.get(image_url, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as fh:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, fh)
    return filename

# get the top artists for the past week
to_time = int(time.time())
from_time = to_time - 60 * 60 * 24 * 7
url = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user=%s&api_key=%s&from=%s&to=%s&format=json" % (lastfm_user, lastfm_api_key, from_time, to_time)
results = http.get(url).json()
artists = results["weeklyartistchart"]["artist"][0:3]

# create the status message
lastfm_link = "https://www.last.fm/user/%s/library/artists?to=%s&from=%s" % (lastfm_user, to_time, from_time)
parts = ["%s (%s)" % (a["name"],  a["playcount"]) for a in artists[0:3]]
msg = "What I've been listening to this week: %s #lastfm\n\n%s" % (
    ", ".join(parts),
    lastfm_link
)

# get artist images
images = []
for artist in artists:
    image = get_image(artist['url'])
    if image:
        images.append(image)

# tweet them
if not debug and twitter_consumer_key:
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    twitter = tweepy.API(auth)
    if len(images) > 0:
        media_ids = [twitter.media_upload(i).media_id_string for i in images]
        twitter.update_status(status=msg, media_ids=media_ids)
    else:
        twitter.update_status(msg)

# twoot them
if not debug and mastodon_access_token:
    m = mastodon.Mastodon(
        api_base_url=mastodon_url,
        client_id=mastodon_client_id,
        client_secret=mastodon_client_secret,
        access_token=mastodon_access_token
    )
    media_ids = [m.media_post(i) for i in images]
    m.status_post(status=msg, media_ids=media_ids)

if debug:
    print(msg)
    for i in images:
        print("-", i)
