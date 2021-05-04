import pandas as pd

from config import Config

TEST = Config.TEST


class DataSequence():

    __unique_words_ids = {}
    __unique_customers_ids = {}
    __next_words_ids = 0
    __next_customers_ids = 0

    def __init__(self, customer, text):
        self.cid = self.get_unique_cid(customer)
        self.unique_words_ids = self.get_unique_words_ids(text)

    def __lt__(self, other):
        return self.cid < other.cid

    def __gt__(self, other):
        return self.cid > other.cid

    def __eq__(self, other):
        return self.cid == other.cid

    @staticmethod
    def unique_words(text):
        """
        Zwraca posortowany zbiór unikalnych wyrazów w tekscie.
        """
        unique_words = set()
        # Wyrazy napisane małymi literami.
        words = text.lower().split()
        for word in words:
            # Usuniecie znakow interpukcyjnych
            word = word.strip('.,!;()[]')
            unique_words.add(word)
        return unique_words

    @classmethod
    def get_unique_cid(cls, customer):
        if customer in cls.__unique_customers_ids:
            return cls.__unique_customers_ids[customer]
        else:
            tmp = cls.__next_customers_ids
            cls.__unique_customers_ids[customer] = tmp
            cls.__next_customers_ids = tmp + 1
            return tmp

    @classmethod
    def get_unique_words_ids(cls, text):
        unique_words = DataSequence.unique_words(text)
        ids = []
        for word in unique_words:
            if word in cls.__unique_words_ids:
                ids.append(cls.__unique_words_ids[word])
            else:
                tmp = cls.__next_words_ids
                cls.__unique_words_ids[word] = tmp
                cls.__next_words_ids = tmp + 1
                ids.append(tmp)
        return sorted(ids)

    @classmethod
    def get_words(cls, id=None):
        if id is None:
            return cls.__unique_words_ids
        for word, word_id in cls.__unique_words_ids.items():
            if word_id == id:
                return word
        return None

    @classmethod
    def get_customers(cls, cid=None):
        if cid is None:
            return cls.__unique_customers_ids
        for customer, customer_id in cls.__unique_customers_ids.items():
            if customer_id == cid:
                return customer
        return None

    @classmethod
    def data_sequence_factory(cls, customers=TEST['customers'],
                              texts=TEST['texts'], path=TEST['path']):
        sequences = []
        raw_data_frame = pd.read_csv(path)
        for index, row in raw_data_frame.iterrows():
            customer = row[customers]
            text = row[texts]
            s = cls(customer, text)
            sequences.append(s)
        return sequences


sequences = DataSequence.data_sequence_factory()
sequences = sorted(sequences)
a = DataSequence.get_words()
b = DataSequence.get_customers()
print(a)
print(b)

for s in sequences:
    ids = s.unique_words_ids
    print(ids)
    c = s.cid
    print(c)
