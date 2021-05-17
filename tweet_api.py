import datetime
import pandas as pd

import tweepy as tw

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
    def collect_tweets(cls, search_word=TWEET['search_word'], items=TWEET['items']):
        # Collect tweets.
        search_words = "{} since:{} until:{} -filter:retweets".format(
            search_word, str(cls.since), str(cls.until))
        tweets_list = tw.Cursor(
            cls.api.search, q=search_words,
            tweet_mode='extended', lang='en').items(items)  
        data = [[tweet.user.screen_name, tweet._json["full_text"]] for tweet in tweets_list]
        return data

    @classmethod
    def save_collected_tweets(cls, data, columns_name=['user', 'text']):
        tweet_data_frame = pd.DataFrame(
            data=data, columns=[TWEET['customers'], TWEET['texts']])
        tweet_data_frame.to_csv(TWEET['output'])


if __name__ == "__main__":

    data = TweetApi.collect_tweets()
    for user_name, text in data:
        print("user ->>> {}\ntext ->>>> {}\n".format(user_name, text))
    TweetApi.save_collected_tweets(data)
