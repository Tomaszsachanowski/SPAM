class CMAP_item():
    
    def __init__(self, word_id):
        self.word_id = word_id
        self.extensions_count = {}

    def add_occurence(self, extension):
        if extension not in self.extensions_count:
            self.extensions_count[extension] = 1 
        else:
            self.extensions_count[extension] += 1

    def get_word_id(self):
        return self.word_id

    def get_extensions(self):
        return self.extensions_count


class CMAP():

    def __init__(self, seq_list, min_sup):
        self.seq_list = seq_list
        self.min_sup = min_sup
        self.cmap_count = []
        self.cmap = {}
        self.build_cmap_s()


    def add_to_cmap_count(self, item, ext):
        citem = next((citem for citem in self.cmap_count if citem.get_word_id() == item), None)
        if citem == None:
            citem = CMAP_item(item)
            citem.add_occurence(ext)
            self.cmap_count.append(citem)
        else:
            citem.add_occurence(ext)


    def set_cmap(self):
        for citem in self.cmap_count:
            extensions_count = citem.get_extensions()
            min_extensions = []
            for ext in extensions_count:
                if extensions_count[ext] >= self.min_sup:
                    min_extensions.append(ext)
            self.cmap[citem.get_word_id()] = min_extensions


    def build_cmap_i(self):
        for sequence in self.seq_list:
            for itemset in sequence:
                for item in itemset:
                    filtered_itemset = filter(lambda ext: (ext > item), itemset)
                    for ext in filtered_itemset:
                        self.add_to_cmap_count(item, ext)

        self.set_cmap()
        print(self.cmap)
        for i in self.cmap_count:
            print("item {}".format(i.get_word_id()))
            print(i.get_extensions())
        return self.cmap


    def build_cmap_s(self):
        for sequence in self.seq_list:
            checked_pairs = []
            itemsets_count = len(sequence)
            for extensions_itemset in range(itemsets_count - 1, -1, -1):
                previous_items = set()
                for items_itemset in range(extensions_itemset - 1, -1, -1):
                    previous_items.update(sequence[items_itemset])
                for ext in sequence[extensions_itemset]:
                    for item in previous_items:
                        if (item, ext) not in checked_pairs:
                            self.add_to_cmap_count(item, ext)
                            checked_pairs.append((item, ext))
        self.set_cmap()
        print(self.cmap)
        for i in self.cmap_count:
            print("item {}".format(i.get_word_id()))
            print(i.get_extensions())
        return self.cmap


def transform_sequences_into_lists(sequences, cids_number):
    seq_list = []
    for i in range(cids_number):
        seq_list.append([])
    for s in sequences:
        seq_list[s.cid].append(s.unique_words_ids)
    print(seq_list)
    return seq_list
