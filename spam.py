import itertools
import numpy as np
import copy

from read_data import DataSequence


class SPAM():

    frequent_items = []
    frequent_patterns = []

    def __init__(self, min_sup, seq_bitmaps):
        """
        @param min_sup: minimalne wsparcie czestego wzorca
        @param seq_bitmaps: baza danych w postaci map bitowych, lista krotek - ([id przedmiotu], [[partycja1], [partycja2], ...])
        """

        self.min_sup = min_sup * len(seq_bitmaps[0][1])
        self.seq_bitmaps = seq_bitmaps


    def dfs_pruning(self, node, s_n, i_n):
        """
        Przeszukuje drzewo w glab, przycinajac je zgodnie z zasada apriori.

        @param node: sekwencja zbiorow elementow (lista list)
        @param s_n: zbior kandydatow do tworzenia dzieci przez krok "S"
        @param i_n: zbior kandydatow do tworzenia dzieci przez krok "I"
        """

        if (s_n == [] and i_n == []):
            return 

        s_temp = []
        i_temp = []

        new_frequent_patterns_s = []
        new_frequent_patterns_i = []

        for i in s_n:
            new_node_bitmap = self.check_if_frequent_s(node, i)
            if new_node_bitmap is not None:
                new_sequence = node[0] + [i]
                new_frequent_patterns_s.append((new_sequence, new_node_bitmap))
                s_temp.append(i)
        
        for new_node in new_frequent_patterns_s:
            self.dfs_pruning(new_node, s_temp, list(filter(lambda x: x[0] > i[0], s_temp)))

        for i in i_n:
            new_node_bitmap = self.check_if_frequent_i(node, i)
            if new_node_bitmap is not None:
                new_sequence = self.i_extend(node[0], i[0])
                new_frequent_patterns_i.append((new_sequence, new_node_bitmap))

        for new_node in new_frequent_patterns_i:
            self.dfs_pruning(new_node, s_temp, list(filter(lambda x: x[0] > i[0], i_temp)))

        self.frequent_patterns = self.frequent_patterns + new_frequent_patterns_s + new_frequent_patterns_i



    def check_if_frequent_s(self, node, i):
        """
        Sprawdza, czy po dodaniu do sekwencji nowego zbioru [i] bedzie czesta i jesli tak, to zwraca mape bitowa nowej sekwencji

        @param node: krotka (sekwencja, mapa bitowa sekwencji)
        @param i: nowy zbior (jednoelementowa lista)
        """
        node_bitmap = self.bitmap_transform(node[1])
        i_bitmap = self.get_bitmap([i])
        return self.check_if_frequent(node_bitmap, i_bitmap)


    def bitmap_transform(self, bitmap):
        """
        Przeksztalca bitmape dla kroku S

        @param bitmap: lista bitow
        """
        transformed_bitmap = []
        for partition in bitmap:
            start_setting_bits = False
            transformed_partition = []
            for bit in partition:
                if start_setting_bits:
                    transformed_partition.append(1)
                else:
                    transformed_partition.append(0)
                if start_setting_bits is False and bit == 1:
                    start_setting_bits = True
            transformed_bitmap.append(transformed_partition)
        return transformed_bitmap


    def check_if_frequent_i(self, node, i):
        """
        Sprawdza, czy po dodaniu do ostatniego zbioru sekwencji nowego elementu "i" bedzie czesta i jesli tak, to zwraca mape bitowa nowej sekwencji

        @param node: krotka (sekwencja, mapa bitowa sekwencji)
        @param i: nowy element
        """
        node_bitmap = self.get_bitmap(node[0])
        i_bitmap = self.get_bitmap([i])
        return self.check_if_frequent(node_bitmap, i_bitmap)


    def check_if_frequent(self, bitmap_a, bitmap_b):
        """
        Przeprowadza na bitmapach operacje AND i zwraca nowa bitmape, jesli reprezentuje czesta sekwencje

        @param bitmap_a: bitmapa
        @param bitmap_b: bitmapa
        """
        new_node_bitmap = self.and_partitions(bitmap_a, bitmap_b)
        if (self.count_support(new_node_bitmap) >= self.min_sup):
            return new_node_bitmap
        return None


    def i_extend(self, sequence, i):
        """
        Dodaje element do sekwencji wedlug kroku I (do ostatniego zbioru)

        @param sequence: sekwecja
        @param i: element
        """
        new_sequence = copy.deepcopy(sequence)
        new_sequence[-1].append(i)
        return new_sequence


    def get_bitmap(self, sequence):
        """
        Zwraca bitmape danej sekwencji, jesli zostala wczesniej utoworzona

        @param sequence: sekwecja
        """
        for seq_b in self.seq_bitmaps:
            if seq_b[0] == sequence:
                return seq_b[1]
        raise ValueError('nieznana sekwencja')

    def and_partitions(self, bitmap_a, bitmap_b):
        """
        Operacja AND na bitmapach zlozonych z partycji

        @param bitmap_a: bitmapa
        @param bitmap_b: bitmapa
        """
        bitmap_ab = []
        for (partition_a, partition_b) in zip(bitmap_a, bitmap_b):
            bitmap_ab.append(np.bitwise_and(partition_a, partition_b))
        return bitmap_ab
    
    def count_support(self, sequence_bitmap):
        """
        Zlicza wsparcie (bezwzgledne)

        @param sequence_bitmap: krotka (sekwencja, mapa bitowa sekwencji)
        """
        support = 0
        for partition in sequence_bitmap:
            if 1 in partition:
                support += 1
        return support


    def filter_unfrequent_sequences(self):
        """
        Usuwa z bazy wzorce, ktore nie sa czeste (przeznaczona do przefiltrowania jednoelementowych wzorcow podanych przy inicjalizacji)
        """
        new_seq_bitmaps = []
        for seq_b in self.seq_bitmaps:
            if self.count_support(seq_b[1]) >= self.min_sup:
                new_seq_bitmaps.append(seq_b)
                self.frequent_items.append(seq_b[0][0])
                self.frequent_patterns.append(seq_b)
        self.seq_bitmaps = new_seq_bitmaps


    def spam(self):
        """
        Uruchamia algorytm
        """
        self.filter_unfrequent_sequences()
        for seq_b in self.seq_bitmaps:
            i_n = []
            for item in self.frequent_items: 
                if item[0] > seq_b[0][0][0]: # seq_b[0][0][0] - pierwszy element pierwszego zbioru w sekwencji, np. ([[0]], mapa bitowa) -> 0
                    i_n += [item]
            self.dfs_pruning(seq_b, self.frequent_items, i_n)

        return self.frequent_patterns
        

# For test
from read_data import generate_simple_sequeneces
from read_data import generate_test_sequeneces
from bitmap import generate_words_bitmaps


def translate_patterns(frequent_patterns):
    translated_patterns = []
    for pattern in frequent_patterns:
        translated_sequence = []
        for itemset in pattern[0]:
            translated_itemset = []
            for item in itemset:
                translated_itemset.append(DataSequence.get_words(item))
            translated_sequence.append(translated_itemset)
        translated_patterns.append(translated_sequence)
    return translated_patterns

    
if __name__ == "__main__":
#    sequences = generate_simple_sequeneces()
#    generate_test_sequeneces(number_of_items, number_of_sequences, number_of_customers, min_items_in_transaction, max_items_in_transaction)
    sequences = generate_test_sequeneces(10, 3, 1, 4, 6)
    bitmaps_for_words_ids = generate_words_bitmaps(sequences)

    spam_alg = SPAM(0.5, bitmaps_for_words_ids)
    frequent_patterns = spam_alg.spam()

    with open("frequent_patterns", 'w') as file: 
        for pattern in translate_patterns(frequent_patterns):
            file.write(str(pattern) + '\n')


