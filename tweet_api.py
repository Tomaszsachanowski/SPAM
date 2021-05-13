import os
import tweepy as tw
import pandas as pd
import datetime

consumer_key= '4Aq6KSNh7oke2DVWIFuq4Vdae'
consumer_secret= 'TRu8Y9ZYystbQs6biF8KR3DRM8k1GbTRnsZQNuKAuhamjl1Zl8'
access_token= '1392905688318361603-k7lYPGzirhJpqhYd8RCDdQt4cW8jVE'
access_token_secret= 's4lwFsSPrdJN2qWCmqlUrnA5DpHcf95XXlNpFAM16fN7U'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


today = datetime.date.today()
yesterday= today - datetime.timedelta(days=1)

search_words = "#wildfires"
date_since = "2018-11-16"

# Collect tweets
tweets_list = tw.Cursor(
    api.search, q="#Covid-19 since:" + str(yesterday)+ " until:" + str(today),
    tweet_mode='extended', lang='en').items(10)

output = []
for tweet in tweets_list:
    text = tweet._json["full_text"]
    print(text)
    favourite_count = tweet.favorite_count
    retweet_count = tweet.retweet_count
    created_at = tweet.created_at
    
    line = {
        'text' : text,
        'favourite_count' : favourite_count,
        'retweet_count' : retweet_count,
        'created_at' : created_at}
    output.append(line)
    print(line)
    print()

df = pd.DataFrame(output)
df.to_csv('output.csv')