#!/usr/bin/env python3

import click


from read_data import DataSequence
from bitmap import generate_words_bitmaps
from spam import SPAM, translate_patterns
from config import Config

TEST = Config.TEST

@click.group()
def spam_cli():
    """
        Command Line Interpreter for SPAM algoritm

        cli_spam minsup <int> data_path <str>
    """
    pass

@spam_cli.command(
help="Start spam algoritm minsup",
short_help="Start spam algoritm"
)
@click.argument('minsup', nargs=1, required=True, type=int)
@click.argument('data_path', nargs=1, required=True, type=str)
def start(minsup, data_path):
    sequences = DataSequence.data_sequence_factory(
        customers=TEST['customers'], texts=TEST['texts'], path=data_path)
    bitmaps_for_words_ids = generate_words_bitmaps(sequences)
    spam_alg = SPAM(minsup, bitmaps_for_words_ids)
    frequent_patterns = spam_alg.spam()

    with open("frequent_patterns", 'w') as file: 
        for pattern in translate_patterns(frequent_patterns):
            file.write(str(pattern) + '\n')

# Przykład użycia python cli_spam start 2 /data/test_simple.csv
if __name__ == "__main__":
    spam_cli()





