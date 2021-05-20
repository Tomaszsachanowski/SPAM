# For test
import time
import matplotlib.pyplot as plt

from read_data import generate_simple_sequeneces, generate_test_sequeneces
from bitmap import generate_words_bitmaps
from spam import SPAM


def measure_spam(number_of_items, number_of_sequences,
              number_of_customers, min_items_in_transaction,
              max_items_in_transaction, min_sup):
    time_result = []
    for i in range(10):
        print("probka {}".format(i))
        sequences = generate_test_sequeneces(
            number_of_items, number_of_sequences, number_of_customers,
            min_items_in_transaction, max_items_in_transaction)
        bitmaps_for_words_ids = generate_words_bitmaps(sequences)
        spam_alg = SPAM(min_sup, bitmaps_for_words_ids)

        start = time.time()
        spam_alg.spam()
        end = time.time()
        result = end - start
        time_result.append(result)

    mean = sum(time_result)/len(time_result)
    return mean


def test_one_sequence_different_itemset_numbers():
    # jedna sekwencja, rozna ilosc zbiorów
    sequence_lengths = range(1, 6)
    execution_times = [measure_spam(10, i, 1, 4, 6, 0.5) for i in sequence_lengths]
 
    fig, ax = plt.subplots()
    ax.plot(sequence_lengths, execution_times)

    ax.set(xlabel='number of itemsets', ylabel='time (s)',
        title='One sequence on input')
    ax.grid()

    fig.savefig("images/spam_10_i_1_4_6_05.png")
    plt.show()


def test_different_item_numbers():
    # jeden klient, rozne dlugosci sekwencji
    item_numbers = range(3, 30)
    execution_times = [measure_spam(i, 3, 5, int(i/3), int(i/3), 0.5) for i in item_numbers]

    fig, ax = plt.subplots()
    ax.plot(item_numbers, execution_times)

    ax.set(xlabel='number of items', ylabel='time (s)',
        title='Differing item numbers')
    ax.grid()

    fig.savefig("images/spam_i_3_5_4_6_05.png")
    plt.show()


def test_different_sequence_numbers():
    # jeden klient, rozne dlugosci sekwencji
    sequence_numbers = range(10, 30)
    execution_times = [measure_spam(10, 5, i, 4, 6, 0.5) for i in sequence_numbers]

    fig, ax = plt.subplots()
    ax.plot(sequence_numbers, execution_times)

    ax.set(xlabel='number of customers (input sequences)', ylabel='time (s)',
        title='Differing number of input sequnces')
    ax.grid()

    fig.savefig("images/spam_10_5_i_4_6_05.png")
    plt.show()


if __name__ == "__main__":
    test_one_sequence_different_itemset_numbers()
    test_different_sequence_numbers()
    test_different_item_numbers()