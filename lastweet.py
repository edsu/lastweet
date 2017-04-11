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
import tweepy
import mastodon
import requests
import urllib.request

# get some environment variables
e = os.environ.get
twitter_consumer_key = e('TWITTER_CONSUMER_KEY')
twitter_consumer_secret = e('TWITTER_CONSUMER_SECRET')
twitter_access_token = e('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = e('TWITTER_ACCESS_TOKEN_SECRET')
lastfm_api_key = e('LASTFM_KEY')
lastfm_user = e('LASTFM_USER')
mastodon_client_id = e('MASTODON_CLIENT_ID')
mastodon_client_secret = e('MASTODON_CLIENT_SECRET')
mastodon_access_token = e('MASTODON_ACCESS_TOKEN')

# get the top artists for the past week
to_time = int(time.time())
from_time = to_time - 60 * 60 * 24 * 7
url = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user=%s&api_key=%s&from=%s&to=%s&format=json" % (lastfm_user, lastfm_api_key, from_time, to_time)
results = requests.get(url).json()
artists = results["weeklyartistchart"]["artist"]

status = "My top 3 #lastfm artists:"
parts = ["%s (%s)" % (a["name"],  a["playcount"]) for a in artists[0:3]]
msg = "My top 3 #lastfm artists: " + ", ".join(parts)

# tweet them
if twitter_consumer_key:
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    twitter = tweepy.API(auth)
    twitter.update_status(msg)

# twoot them
if mastodon_access_token:
    m = mastodon.Mastodon(
        client_id=mastodon_client_id,
        client_secret=mastodon_client_secret,
        access_token=mastodon_access_token
    )
    m.status_post(msg)
