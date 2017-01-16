#!/usr/bin/env python

import os
import sys
import json
import time
import tweepy
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

# get the top artists for the past week
to_time = int(time.time())
from_time = to_time - 60 * 60 * 24 * 7
url = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user=%s&api_key=%s&from=%s&to=%s&format=json" % (lastfm_user, lastfm_api_key, from_time, to_time)
results = requests.get(url).json()
artists = results["weeklyartistchart"]["artist"]

# tweet them
status = "My top 3 #lastfm artists:"
parts = ["%s (%s)" % (a["name"],  a["playcount"]) for a in artists[0:3]]
msg = "My top 3 #lastfm artists: " + ", ".join(parts)
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter = tweepy.API(auth)
twitter.update_status(msg)
