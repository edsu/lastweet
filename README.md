Send status updates on Twitter and Mastodon for for the top artists you've
listened to in the past 7 days using LastFM. Here's an example tweet:

<img src="https://i.imgur.com/v8mdziu.png">

To run this first install lastweet:

    pip install lastweet

Then you'll need set a bunch of things in your environment. Since it's 
convenient to run this from cron every week create a file that sets all 
the variables and then runs lastweet.

```
export LASTFM_USER="inkdroid"
export LASTFM_KEY="CHANGEME"
export LASTFM_SECRET="CHANGEME"
export TWITTER_CONSUMER_KEY="CHANGEME"
export TWITTER_CONSUMER_SECRET="CHANGEME"
export TWITTER_ACCESS_TOKEN="CHANGEME"
export TWITTER_ACCESS_TOKEN_SECRET="CHANGEME"
export MASTODON_CLIENT_ID="CHANGEME"
export MASTODON_CLIENT_SECRET="CHANGEME"
export MASTODON_ACCESS_TOKEN="CHANGEME"

lastweet.py
```

