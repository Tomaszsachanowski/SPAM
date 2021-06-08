# For test
import time
import matplotlib.pyplot as plt
import sys

from cmap import CMAP, transform_sequences_into_lists
from read_data import generate_simple_sequeneces, generate_test_sequeneces
from bitmap import generate_words_bitmaps
from spam import SPAM
import timeit
from read_data import DataSequence
from bitmap import generate_words_bitmaps
from spam import SPAM, translate_patterns
from config import Config
from tweet_api import TweetApi

@profile
def measure_memory(sequences, min_sup=0.5):
    bitmaps_for_words_ids = generate_words_bitmaps(sequences)
    seq_list = transform_sequences_into_lists(sequences, len(sequences[0].get_cids()))
    cmap_i = CMAP(seq_list, min_sup*len(seq_list)).build_cmap_i()
    cmap_s = CMAP(seq_list, min_sup*len(seq_list)).build_cmap_s()
    spam_alg = SPAM(min_sup, bitmaps_for_words_ids, cmap_i, cmap_s)
    spam_alg.spam()

def measure_cmap_spam(sequences, min_sup=0.5):
    time_result = []
    for i in range(10):
        bitmaps_for_words_ids = generate_words_bitmaps(sequences)
        seq_list = transform_sequences_into_lists(sequences, len(sequences[0].get_cids()))
        cmap_i = CMAP(seq_list, min_sup*len(seq_list)).build_cmap_i()
        cmap_s = CMAP(seq_list, min_sup*len(seq_list)).build_cmap_s()
        spam_alg = SPAM(min_sup, bitmaps_for_words_ids, cmap_i, cmap_s)
        time_result.append(timeit.timeit(spam_alg.spam, number = 1))
    mean = sum(time_result)/len(time_result)
    return mean

def measure_spam(number_of_items, number_of_sequences,
              number_of_customers, min_items_in_transaction,
              max_items_in_transaction, min_sup):
    time_result = []
    for i in range(100):
        #print("probka {}".format(i))
        sequences = generate_test_sequeneces(
            number_of_items, number_of_sequences, number_of_customers,
            min_items_in_transaction, max_items_in_transaction)
        bitmaps_for_words_ids = generate_words_bitmaps(sequences)
        spam_alg = SPAM(min_sup, bitmaps_for_words_ids)

        # start = time.time()
        # spam_alg.spam()
        # end = time.time()
        # result = end - start
        time_result.append(timeit.timeit(spam_alg.spam, number = 1))

    mean = sum(time_result)/len(time_result)
    return mean


def make_file_name(items, sequences, customers, min_trans, max_trans, min_sup):
    return "images/spam_{items}_{sequences}_{customers}_{min_trans}_{min_trans}_{min_sup}.png".format(
        items = items, sequences = sequences, customers = customers, min_trans = min_trans, max_trans = max_trans, min_sup = min_sup)


def test_one_sequence_different_itemset_numbers():
    # jedna sekwencja, rozna ilosc zbiorów
    sequence_lengths = range(1, 5)
    execution_times = [measure_spam(20, i, 1, 4, 6, 0.5) for i in sequence_lengths]
 
    fig, ax = plt.subplots()
    ax.plot(sequence_lengths, execution_times, 'o', color='black')

    ax.set(xlabel='number of itemsets', ylabel='time (s)',
        title='Execution time with one sequence on input')
    ax.grid()

    fig.savefig(make_file_name('20', 'i', '1', '4', '6', '05'))
    plt.show()


# def test_different_item_numbers():
#     # jeden klient, rozne dlugosci sekwencji
#     item_numbers = range(3, 30)
#     execution_times = [measure_spam(i, 3, 5, int(i/3), int(i/3), 0.5) for i in item_numbers]

#     fig, ax = plt.subplots()
#     ax.plot(item_numbers, execution_times, 'o', color='black')

#     ax.set(xlabel='number of items', ylabel='time (s)',
#         title='Differing item numbers')
#     ax.grid()

#     fig.savefig("images/spam_i_3_5_i3_i3_05.png")
#     plt.show()


def test_different_item_numbers_fixed_itemset_size():
    item_numbers = range(3, 300)
    execution_times = [measure_spam(i, 3, 5, 3, 3, 0.5) for i in item_numbers]

    fig, ax = plt.subplots()
    ax.plot(item_numbers, execution_times, 'o', color='black')

    ax.set(xlabel='number of items', ylabel='time (s)',
        title='Execution time by number of items in dictionary')
    ax.grid()

    fig.savefig(make_file_name('i', '3', '5', '3', '3', '05'))
    plt.show()


def test_different_itemset_size():
    item_numbers = range(1, 10)
    execution_times = [measure_spam(40, 10, 2, i, i, 0.5) for i in item_numbers]

    fig, ax = plt.subplots()
    ax.plot(item_numbers, execution_times, 'o', color='black')

    ax.set(xlabel='number of items', ylabel='time (s)',
        title='Execution time by number of items in itemset')
    ax.grid()

    fig.savefig(make_file_name('40', '4', '2', '10i', '10i', '05'))
    plt.show()


def test_different_sequence_numbers():
    sequence_numbers = range(1, 10)
    execution_times = [measure_spam(10, 5, i, 2, 3, 0.5) for i in sequence_numbers]

    fig, ax = plt.subplots()
    ax.plot(sequence_numbers, execution_times, 'o', color='black')

    ax.set(xlabel='number of customers (input sequences)', ylabel='time (s)',
        title='Execution time by number of input sequnces')
    ax.grid()

    fig.savefig(make_file_name('10', '5', 'i', '2', '3', '05'))
    plt.show()


def test_different_min_sup():
    sequence_numbers = range(1, 9)
    execution_times = [measure_spam(100, 5, 3, 2, 3, 0.1 * i) for i in sequence_numbers]

    fig, ax = plt.subplots()
    ax.plot(list(map(lambda x: x * 0.1, sequence_numbers)), execution_times, 'o', color='black')

    ax.set(xlabel='minimal support', ylabel='time (s)',
        title='Execution time by minimal support')
    ax.grid()

    fig.savefig(make_file_name('100', '5', '3', '2', '3', '0i'))
    plt.show()


def test_tweets():
    execution_times = []
    amount_tweets = [3, 5, 8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35]
    for i in amount_tweets:
        search_word = "#Covid-19"
        items = i
        data = TweetApi.collect_tweets(
            search_word=search_word, items=items)
        TweetApi.save_collected_tweets(data)
        sequences = DataSequence.data_sequence_factory(
            customers="name", texts="text",
            path="data/tweet_output.csv")
        mean_time = measure_cmap_spam(sequences, min_sup=0.5)
        execution_times.append(mean_time)

    fig, ax = plt.subplots()
    ax.plot(amount_tweets, execution_times, 'o', color='black')

    ax.set(xlabel='number of tweets', ylabel='time (s)',
        title='Execution time by number of tweets')
    ax.grid()

    fig.savefig("tweets time")
    plt.show()


def test_tweets_min_sup():
    execution_times = []
    search_word = "#Covid-19"
    items = 30
    data = TweetApi.collect_tweets(
        search_word=search_word, items=items)
    TweetApi.save_collected_tweets(data)
    sequences = DataSequence.data_sequence_factory(
        customers="name", texts="text",
        path="data/tweet_output.csv")

    min_sup = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    for sup in min_sup:

        mean_time = measure_cmap_spam(sequences, min_sup=min_sup)
        execution_times.append(mean_time)

    fig, ax = plt.subplots()
    ax.plot(min_sup, execution_times, 'o', color='red', label="CM-SPAM")

    ax.set(xlabel='minimal support', ylabel='time (s)',
        title='Execution time by minimal support for CM-SPAM')
    ax.grid()
    plt.legend()
    fig.savefig("tweets min sup")
    plt.show()


if __name__ == "__main__":
    #test_one_sequence_different_itemset_numbers()
    #test_different_item_numbers_fixed_itemset_size()
    #test_different_itemset_size()
    #test_different_sequence_numbers()
    #test_different_min_sup()

