# For test
import timeit
import matplotlib.pyplot as plt

from read_data import generate_simple_sequeneces, generate_test_sequeneces
from bitmap import generate_words_bitmaps
from spam import SPAM


def test_spam(number_of_items, number_of_sequences,
              number_of_customers, min_items_in_transaction,
              max_items_in_transaction, min_sup):
    sequences = generate_test_sequeneces(
        number_of_items, number_of_sequences, number_of_customers,
        min_items_in_transaction, max_items_in_transaction)
    bitmaps_for_words_ids = generate_words_bitmaps(sequences)
    SPAM(min_sup, bitmaps_for_words_ids).spam()
    

def test_one_sequence_different_itemset_numbers():
    # jeden klient, rozne dlugosci sekwencji
    sequence_lengths = range(1, 10)
    execution_times = []
    for i in sequence_lengths:
        t = timeit.Timer(lambda: test_spam(10, i, 1, 4, 6, 0.5))
        execution_times.append(
            t.timeit(100)
        )

    fig, ax = plt.subplots()
    ax.plot(sequence_lengths, execution_times)

    ax.set(xlabel='number of itemsets', ylabel='time (s)',
        title='One sequence on input')
    ax.grid()

    fig.savefig("spam_10_i_1_4_6_05.png")
    plt.show()


def test_different_item_numbers():
    # jeden klient, rozne dlugosci sekwencji
    item_numbers = range(3, 30)
    execution_times = []
    for i in item_numbers:
        t = timeit.Timer(lambda: test_spam(i, 3, 5, int(i/3), int(i/3), 0.5))
        execution_times.append(
            t.timeit(100)
        )

    fig, ax = plt.subplots()
    ax.plot(item_numbers, execution_times)

    ax.set(xlabel='number of items', ylabel='time (s)',
        title='Differing item numbers')
    ax.grid()

    fig.savefig("spam_i_3_5_4_6_05.png")
    plt.show()


def test_different_sequence_numbers():
    # jeden klient, rozne dlugosci sekwencji
    sequence_numbers = range(10, 30)
    execution_times = []
    for i in sequence_numbers:
        t = timeit.Timer(lambda: test_spam(10, 5, i, 4, 6, 0.5))
        execution_times.append(
            t.timeit(100)
        )

    fig, ax = plt.subplots()
    ax.plot(sequence_numbers, execution_times)

    ax.set(xlabel='number of customers (input sequences)', ylabel='time (s)',
        title='Differing number of input sequnces')
    ax.grid()

    fig.savefig("spam_10_5_i_4_6_05.png")
    plt.show()


if __name__ == "__main__":
    test_one_sequence_different_itemset_numbers()
    #test_different_sequence_numbers()
    #test_different_item_numbers()