import bitmap
import itertools

class SPAM():

    def __init__(self, min_sup, seq_bitmaps):
        self.min_sup = min_sup
        self.seq_bitmaps = seq_bitmaps


    def dfs_pruning(self, node, s_n, i_n):
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

        for i in s_n:
            if check_if_frequent_s(node, i):
                s_temp.append(i)
        
        for i in s_temp:
            dfs_pruning(node.append([i]), s_temp, list(filter(lambda x: x > i, s_temp)))

        for i in i_n:
            if check_if_frequent_i(node, i):
                i_temp.append(i)

        for i in i_temp:
            dfs_pruning(i_extend(node, i), s_temp, list(filter(lambda x: x > i, i_temp)))



    def check_if_frequent_s(self, node, i):
        node_bitmap = bitmap_transform(get_bitmap(node))
        i_bitmap = get_bitmap([i])
        return self.check_if_frequent(self, node_bitmap, i_bitmap)


    def check_if_frequent_i(self, node, i):
        node_bitmap = get_bitmap(node)
        i_bitmap = get_bitmap([i])
        return self.check_if_frequent(self, node_bitmap, i_bitmap)


    def check_if_frequent(self, bitmap_a, bitmap_b):
        new_sequence_bitmap = and_partitions(bitmap_a, bitmap_b)
        if (count_support(new_node_bitmap) >= self.min_sup):
            return True
        return False


    def i_extend(self, node, i):
        extended_itemset = (node[-1]).append(i)
        node[-1] = extended_itemset
        return node


    def add_bitmap(self, node, bitmap):
        self.seq_bitmaps[node] = bitmap

    def get_bitmap(self, node):
        if node in self.seq_bitmaps:
           return self.seq_bitmaps[node]
        raise ValueError('nieznana sekwencja')

    def and_partitions(self, bitmap_a, bitmap_b):
        bitmap_ab = []
        for (partition_a, partition_b) in zip(bitmap_a, bitmap_b):
            bitmap_ab.append(np.bitwise_and(a, b))
    