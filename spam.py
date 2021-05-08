import numpy as np

class SPAM():

    def __init__(self, min_sup):
        self.min_sup = min_sup


    def dfs_pruning(cls, node = [], s_n, i_n):
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
            dfs_pruning(node.append([i]), s_temp, list(filter(lambda x: word_gt(x, i), s_temp)))

        for i in i_n:
            if check_if_frequent_i(node, i):
                i_temp.append(i)

        for i in i_temp:
            dfs_pruning(i_extend(node, i), s_temp, list(filter(lambda x: word_gt(x, i), i_temp)))



    def check_if_frequent_s(cls, node, i):
        node_bitmap = bitmap_transform(get_bitmap(node))
        i_bitmap = get_bitmap([i])
        return cls.check_if_frequent(cls, node_bitmap, i_bitmap)


    def check_if_frequent_i(cls, node, i):
        node_bitmap = get_bitmap(node)
        i_bitmap = get_bitmap([i])
        return cls.check_if_frequent(cls, node_bitmap, i_bitmap)


    def check_if_frequent(cls, bitmap_a, bitmap_b):
        new_sequence_bitmap = and_partitions(bitmap_a, bitmap_b)
        if (count_support(new_node_bitmap) >= cls.min_sup):
            return True
        return False


    def i_extend(cls, node, i):
        extended_itemset = (node[-1]).append(i)
        node[-1] = extended_itemset
        return node


    dodanie slownika 

    zainicjowanie i dodawanie bitmap

    word_gt(x, i)

    get_bitmap(node)

    and_partitions(node_bitmap, i_bitmap) // np.bitwise_and(a, b)