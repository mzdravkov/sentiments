import os
import tweepy

client = tweepy.Client(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        bearer_token=os.environ['TWITTER_BEARER_TOKEN'])

tweets = []

for tweet in tweepy.Paginator(client.search_recent_tweets,
        'cop26 -is:retweet lang:en',
        max_results=10,
        ).flatten(30):
    print(len(tweet.text))
    print(tweet.text)
    print('===')
    tweets.append(tweet)

# print([t.text for t in tweets])

