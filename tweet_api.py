import os
import tweepy as tw
import pandas as pd
import datetime

import re
# from wordsegment import load, segment
# load()
from autocorrect import spell

from config import Config

TWEET = Config.TWEET

class TweetApi():

    auth = tw.OAuthHandler(
            TWEET['CONSUMER_KEY'], TWEET['CONSUMER_SECRET'])
    auth.set_access_token(
            TWEET['ACCESS_TOKEN'], TWEET['ACCESS_SECRET'])
    api = tw.API(auth, wait_on_rate_limit=True)

    until = datetime.date.today()
    since = until - datetime.timedelta(days=1)

    @classmethod
    def collect_tweets(cls, search_word="#Covid-19", items=10):
        # Collect tweets.
        search_words = "{} since:{} until:{} -filter:retweets".format(
            search_word, str(cls.since), str(cls.until))
        tweets_list = tw.Cursor(
            cls.api.search, q=search_words, tweet_mode='extended',lang='en').items(items)
        data = []
        for tweet in tweets_list:
            text = tweet._json["full_text"]
            user_name = tweet.user.screen_name
            print(text)
            text = cls.preprocessing(text)

            data.append([user_name, text])   
        # data = [[tweet.user.screen_name, tweet._json["full_text"]] for tweet in tweets_list]
        return data

    @staticmethod
    def preprocessing(text):
        text = re.sub(r'^https?:\/\/(www\.)?[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '', text, flags=re.MULTILINE)
        text = re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '', text, flags=re.MULTILINE)
        text = ' '.join(re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', text).split())
        text = ' '.join([spell(word) for word in text.split()])
        text = re.sub(r'\d', '', text)
        text = text.lower()
        return text

    @classmethod
    def save_collected_tweets(cls, data, columns_name=['user', 'text']):
        tweet_data_frame = pd.DataFrame(
            data=data, columns=[TWEET['CID'], TWEET['ITEMS']])
        tweet_data_frame.to_csv(TWEET['OUTPUT'])



data = TweetApi.collect_tweets()
for user_name, text in data:
    print("user ->>> {}\ntext ->>>> {}\n".format(user_name, text))
TweetApi.save_collected_tweets(data)
