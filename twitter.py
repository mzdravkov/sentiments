import os
import tweepy

client = tweepy.Client(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        bearer_token=os.environ['TWITTER_BEARER_TOKEN'])

# tweets = []

# for tweet in tweepy.Paginator(
#         client.search_recent_tweets,
#         'cop26 -is:retweet lang:en',
#         max_results=10,
#         tweet_fields=['id', 'text', 'created_at']
#         ).flatten(limit=10):
#     print(tweet.id)
#     print(tweet.created_at)
#     print(dir(tweet))
#     print(len(tweet.text))
#     print(tweet.text)
#     print('===')
#     tweets.append(tweet)


# print([t.text for t in tweets])

def search_tweets(query, limit=250):
    final_query = query + ' -is:retweet lang:en'
    tweets = tweepy.Paginator(
            client.search_recent_tweets,
            final_query,
            max_results=100,
            tweet_fields=['id', 'text', 'created_at']
            ).flatten(limit=limit)
    return list(tweets)

