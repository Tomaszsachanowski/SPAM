import matplotlib.pyplot as plt
import math

from read_data import DataSequence
from bitmap import generate_words_bitmaps
from spam import SPAM, translate_patterns


def barplot(x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots()
    ax.bar(x, y, color='g')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    # fig.savefig("images/ilosc_wzorcow_długośc")
    plt.show()

def histogram(x, title, xlabel, ylabel,
              density=True, facecolor='g', alpha=0.75):
    fig, ax = plt.subplots()
    ax.hist(x, density=True, facecolor='g', alpha=0.75)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    # fig.savefig("images/czestosc_wzorcow_długośc")
    plt.show()

def vizualization_amount_items_patterns(translate_patterns):
    counter = {}
    a = []
    for pattern in translate_patterns:
        count = 0
        for items in pattern:
            count = count + len(items)
        
        a.append(count)
        if count not in list(counter.keys()):
            counter[count] = 1
        else:
            counter[count] = counter[count] + 1
    x = list(counter.keys())
    y = list(counter.values())
    barplot(x, y, "Ilosc wzorcow o danej ilosci elementow.",
            "ilosc elementow", "ilosc wozorcow")
    histogram(a, "Histogram rozkładu ilosc wzorcow o danej ilosci elementow",
              "ilosc elementow", "Częstość")

def vizualization_frequent_patterns_lenght(translate_patterns):
    counter = {}
    a = []
    for pattern in translate_patterns:
        lenght = len(pattern)
        a.append(lenght)
        if lenght not in list(counter.keys()):
            counter[lenght] = 1
        else:
            counter[lenght] = counter[lenght] + 1
    x = list(counter.keys())
    y = list(counter.values())
    barplot(x, y, "Ilosc znalezionych wzorcow o danej długości.",
            "dlugosc", "ilosc")
    histogram(a, "Histogram rozkładu długości wzorców",
              "dłguość", "Częstość")


if __name__ == "__main__":
    sequences = DataSequence.data_sequence_factory(
        customers="name", texts="text",
        path="data/test_simple.csv")
    bitmaps_for_words_ids = generate_words_bitmaps(sequences)

    spam_alg = SPAM(0.5, bitmaps_for_words_ids)
    frequent_patterns = spam_alg.spam()

    with open("frequent_patterns", 'w') as file: 
        for pattern in translate_patterns(frequent_patterns):
            file.write(str(pattern) + '\n')

    vizualization_frequent_patterns_lenght(translate_patterns(frequent_patterns))
    vizualization_amount_items_patterns(translate_patterns(frequent_patterns))