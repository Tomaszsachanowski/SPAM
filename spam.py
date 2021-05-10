import itertools
import numpy as np

class SPAM():

    frequent_items = []
    frequent_patterns = []

    def __init__(self, min_sup, seq_bitmaps):
        self.min_sup = min_sup * len(seq_bitmaps)
        self.seq_bitmaps = seq_bitmaps
        print(self.min_sup)


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
                new_sequence = node[0] + [[i]]
                new_frequent_patterns_s.append((new_sequence, new_node_bitmap))
                s_temp.append(i)
        
        for new_node in new_frequent_patterns_s:
            self.dfs_pruning(new_node, s_temp, list(filter(lambda x: x > i, s_temp)))

        for i in i_n:
            new_node_bitmap = self.check_if_frequent_i(node, i)
            if new_node_bitmap is not None:
                new_sequence = self.i_extend(node[0], i)
                new_frequent_patterns_i.append((new_sequence, new_node_bitmap))
                i_temp.append(i)

        for new_node in new_frequent_patterns_i:
            self.dfs_pruning(new_node, s_temp, list(filter(lambda x: x > i, i_temp)))

        self.frequent_patterns = self.frequent_patterns + new_frequent_patterns_s + new_frequent_patterns_i



    def check_if_frequent_s(self, node, i):
        node_bitmap = self.bitmap_transform(node[1])
        i_bitmap = self.get_bitmap([i])
        return self.check_if_frequent(node_bitmap, i_bitmap)


    def bitmap_transform(self, bitmap):
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
        node_bitmap = self.get_bitmap(node[0])
        i_bitmap = self.get_bitmap([i])
        return self.check_if_frequent(node_bitmap, i_bitmap)


    def check_if_frequent(self, bitmap_a, bitmap_b):
        new_node_bitmap = self.and_partitions(bitmap_a, bitmap_b)
        if (self.count_support(new_node_bitmap) >= self.min_sup):
            return new_node_bitmap
        return None


    def i_extend(self, sequence, i):
        new_sequence = sequence.copy()
        new_sequence[-1].append(i)
        return new_sequence


    def add_bitmap(self, node, bitmap):
        self.seq_bitmaps.append((node, bitmap))

    def get_bitmap(self, sequence):
        for seq_b in self.seq_bitmaps:
            if seq_b[0] == sequence:
                return seq_b[1]
        raise ValueError('nieznana sekwencja')

    def and_partitions(self, bitmap_a, bitmap_b):
        bitmap_ab = []
        for (partition_a, partition_b) in zip(bitmap_a, bitmap_b):
            bitmap_ab.append(np.bitwise_and(partition_a, partition_b))
        return bitmap_ab
    
    def count_support(self, sequence_bitmap):
        support = 0
        for partition in sequence_bitmap:
            if 1 in partition:
                support += 1
        return support


    def filter_unfrequent_sequences(self):
        new_seq_bitmaps = []
        for seq_b in self.seq_bitmaps:
            if self.count_support(seq_b[1]) >= self.min_sup:
                new_seq_bitmaps.append(seq_b)
                self.frequent_items.append(seq_b[0][0])
                self.frequent_patterns.append(seq_b)
        self.seq_bitmaps = new_seq_bitmaps


    def spam(self):
        self.filter_unfrequent_sequences()
        for seq_b in self.seq_bitmaps:
            self.dfs_pruning(seq_b, self.frequent_items, list(filter(lambda x: x > seq_b[0][0], self.frequent_items)))
