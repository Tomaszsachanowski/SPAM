#!/usr/bin/env python3

import click

from read_data import DataSequence
from bitmap import generate_words_bitmaps
from spam import CMSPAM, translate_patterns
from config import Config
from tweet_api import TweetApi
import cmap


TEST = Config.TEST
TWEET = Config.TWEET


@click.group()
def spam_cli():
    """
        Command Line Interpreter for CMSPAM algoritm

        cli_spam start minsup <int> data_path <str>
        cli_spam get_tweets search_word <str> items <int>

    """
    pass

@spam_cli.command(
help="Start spam algoritm minsup",
short_help="Start spam algoritm"
)
@click.argument('minsup', nargs=1, required=True, type=float)
@click.argument('data_path', nargs=1, required=True, type=str)
def start(minsup, data_path):
    sequences = DataSequence.data_sequence_factory(
        customers=TEST['customers'], texts=TEST['texts'], path=data_path)
    bitmaps_for_words_ids = generate_words_bitmaps(sequences)
    seq_list = cmap.transform_sequences_into_lists(sequences, len(sequences[0].get_cids()))
    cmap_i = cmap.CMAP(seq_list, minsup*len(seq_list)).build_cmap_i()
    cmap_s = cmap.CMAP(seq_list, minsup*len(seq_list)).build_cmap_s()
    spam_alg = CMSPAM(minsup, bitmaps_for_words_ids, cmap_i, cmap_s)
    frequent_patterns = spam_alg.spam()

    with open("frequent_patterns", 'w') as file: 
        for pattern in translate_patterns(frequent_patterns):
            file.write(str(pattern) + '\n')


@spam_cli.command(
    help="Get tweets from tweeter",
    short_help="Get tweets from tweeter")
@click.argument('search_word', type=str, default=TWEET['search_word'])
@click.argument('items', type=int, default=TWEET['items'])
@click.argument('minsup', nargs=1, required=True, type=float)
def get_tweets(minsup, search_word, items):
    data = TweetApi.collect_tweets(search_word=search_word, items=items)
    TweetApi.save_collected_tweets(data)
    sequences = DataSequence.data_sequence_factory(
        customers=TEST['customers'], texts=TEST['texts'], path=TWEET['output'])
    bitmaps_for_words_ids = generate_words_bitmaps(sequences)
    seq_list = cmap.transform_sequences_into_lists(sequences, len(sequences[0].get_cids()))
    cmap_i = cmap.CMAP(seq_list, minsup*len(seq_list)).build_cmap_i()
    cmap_s = cmap.CMAP(seq_list, minsup*len(seq_list)).build_cmap_s()
    spam_alg = CMSPAM(minsup, bitmaps_for_words_ids, cmap_i, cmap_s)
    frequent_patterns = spam_alg.spam()

    with open("frequent_patterns_tt", 'w') as file: 
        for pattern in translate_patterns(frequent_patterns):
            file.write(str(pattern) + '\n')

# Przykład użycia python cli_spam start 2 /data/test_simple.csv
# Przykład użycia python cli_spam get-tweets /#Coivd-19 10
if __name__ == "__main__":
    spam_cli()





