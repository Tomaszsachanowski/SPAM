import bitmap
import itertools

class SPAM():

    frequent_items = []
    frequent_patterns = []

    def __init__(self, min_sup, seq_bitmaps):
        self.min_sup = min_sup * len(seq_bitmaps)
        self.seq_bitmaps = seq_bitmaps


    def dfs_pruning(self, node, s_n, i_n, last_greatest_item):
        """
        Przeszukuje drzewo w glab, przycinajac je zgodnie z zasada apriori.

        @param node: sekwencja zbiorow elementow (lista list)
        @param s_n: zbior kandydatow do tworzenia dzieci przez krok "S"
        @param i_n: zbior kandydatow do tworzenia dzieci przez krok "I"
        """

        if (s_n == [] or i_n == []):
            print("Search complete")
            return 

        s_temp = []
        i_temp = []

        new_frequent_patterns_s = []
        new_frequent_patterns_i = []

        for i in s_n:
            new_node_bitmap = check_if_frequent_s(node, i)
            if new_node_bitmap is not None:
                new_node = node.append([i])
                self.new_frequent_patterns_s.append((new_node, node_bitmap))
                s_temp.append(i)
        
        for i in s_temp:
            self.dfs_pruning(node.append([i]), s_temp, list(filter(lambda x: x > i, s_temp)))

        for i in i_n:
            node_bitmap = check_if_frequent_i(node, i)
            if node_bitmap is not None:
                self.new_frequent_patterns_i.append((node, node_bitmap))
                i_temp.append(i)

        for i in i_temp:
            self.dfs_pruning(i_extend(node, i), s_temp, list(filter(lambda x: x > i, i_temp)))

        self.frequent_patterns = self.frequent_patterns + new_frequent_patterns_s + new_frequent_patterns_i



    def check_if_frequent_s(self, node, i):
        node_bitmap = self.bitmap_transform(get_bitmap(node))
        i_bitmap = self.get_bitmap([i])
        return self.check_if_frequent(self, node_bitmap, i_bitmap)


    def bitmap_transform(bitmap):
        transformed_bitmap = []
        start_setting_bits = False
        for bit in bitmap:
            if start_setting_bits:
                transformed_bitmap.append(1)
            else:
                transformed_bitmap.append(0)
            if start_setting_bits is False and bit == 1:
                start_setting_bits = True


    def check_if_frequent_i(self, node, i):
        node_bitmap = self.get_bitmap(node)
        i_bitmap = self.get_bitmap([i])
        return self.check_if_frequent(self, node_bitmap, i_bitmap)


    def check_if_frequent(self, bitmap_a, bitmap_b):
        new_sequence_bitmap = self.and_partitions(bitmap_a, bitmap_b)
        if (self.count_support(new_node_bitmap) >= self.min_sup):
            return new_node_bitmap
        return None


    def i_extend(self, node, i):
        extended_itemset = (node[-1]).append(i)
        node[-1] = extended_itemset
        return node


    def add_bitmap(self, node, bitmap):
        self.seq_bitmaps.append((node, bitmap))

    def get_bitmap(self, node):
        for seq_b in self.seq_bitmaps:
            if seq_b[0] == node:
                return seq_b[1]
        raise ValueError('nieznana sekwencja')

    def and_partitions(self, bitmap_a, bitmap_b):
        bitmap_ab = []
        for (partition_a, partition_b) in zip(bitmap_a, bitmap_b):
            bitmap_ab.append(np.bitwise_and(a, b))
    
    def count_support(sequence_bitmap):
        bitmap = sequence_bitmap[1]
        support = 0
        for partition in bitmap:
            if 1 in partition:
                support += 1
        return support


    def filter_unfrequent_sequences():
        new_seq_bitmaps = []
        for seq_b in seq_bitmaps:
            if count_support(seq_b) >= min_sup:
                new_seq_bitmaps.append(seq_b)
                self.frequent_items.append(seq_b[0])
                self.frequent_patterns.append(seq_b)
        self.seq_bitmaps = new_seq_bitmaps


    def spam():
        filter_unfrequent_sequences()
        for seq_b in seq_bitmaps:
            one_item_sequence = seq_b[0][0]
            self.dfs_pruning(self, seq_b, s_n, i_n, one_item_sequence)
