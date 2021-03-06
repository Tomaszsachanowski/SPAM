import pandas as pd
import re


from autocorrect import Speller
import nltk
from nltk.corpus import words

from config import Config

TEST = Config.TEST
nltk.download('words')
WORD_LIST = words.words()
SPELL = Speller(lang='en')

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
    def preprocessing(text):
        text = text.replace("’", "").replace("'", "")
        text = re.sub(
            r'^https?:\/\/(www\.)?[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)',
            '', text, flags=re.MULTILINE)
        text = re.sub(
            r'[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)',
            '', text, flags=re.MULTILINE)
        text = ' '.join(
            re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',
            ' ', text).split())
        text = ' '.join([SPELL(word) for word in text.split()])
        text = re.sub(r'\d', '', text)
        text = text.lower()
        return text

    @staticmethod
    def unique_words(text):
        """
        Zwraca posortowany zbiór unikalnych wyrazów w tekscie.
        """
        clear_text = DataSequence.preprocessing(text)
        unique_words = set()
        # Wyrazy napisane małymi literami.
        words = clear_text.split()
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
        return sorted(sequences)

    @classmethod
    def refresh(cls):
        cls.__unique_words_ids = {}
        cls.__unique_customers_ids = {}
        cls.__next_words_ids = 0
        cls.__next_customers_ids = 0


## Only for test generete simple sequences
import random

def generate_simple_sequeneces():
    sequences = []
    # Liczba utoworzonych sekwencji
    max_sequences = 10
    # Zbiór elementów jakie mogą wystąpić
    group_of_texts = ['a', 'b', 'c', 'd', 'e', 'f']
    # Kraje jakie mogą wystąpić
    group_of_customers = ["Poland", "USA", "France", "Germany"]
    for i in range(max_sequences):
        customer =  random.choice(group_of_customers)
        # losuje jak długa będzie sekwencja
        leters_to_select = random.randint(1, len(group_of_texts))
        # losuje odpowiednia liczbę liter
        text_list = random.sample(group_of_texts, leters_to_select)
        # Tworzę z liter wyrazy jedno literowe do klasy przetwarzającej
        text = ' '.join(text_list)
        s = DataSequence(customer=customer, text=text)
        # print("{} ->>>> ({})".format(s.cid, s.unique_words_ids))
        sequences.append(s)
    # print("CIDS ->>>> {}".format(DataSequence.get_customers()))
    # print("Word_IDS ->>>> {}".format(DataSequence.get_words()))
    return sorted(sequences)


def generate_test_sequeneces(number_of_items, number_of_sequences,
                             number_of_customers, min_items_in_transaction,
                             max_items_in_transaction):
   # print("Start generate")
    # print("CIDS ->>>> {}".format(DataSequence.get_customers()))
    # print("Word_IDS ->>>> {}".format(DataSequence.get_words()))

    DataSequence.refresh()
    sequences = []
    # Wyrazy w jezyku angielskim
    items = random.sample(WORD_LIST, number_of_items)

    for i in range(number_of_sequences):
        customer = chr(random.randint(65, 65 + number_of_customers - 1))
        text_list = random.sample(items, k=random.randint(min_items_in_transaction, max_items_in_transaction))
        # Tworze z wuylosowanych wyrazow tekst dla klasy przetwarzajacej
        text = ' '.join(text_list)  
        s = DataSequence(customer=customer, text=text)
        # print("Customer: {} ->> tekst: {}".format(customer, text))
        # print("{} ->>>> ({})".format(s.cid, s.unique_words_ids))
        sequences.append(s)
    # print("Stop generate")
    # print("CIDS ->>>> {}".format(DataSequence.get_customers()))
    # print("Word_IDS ->>>> {}".format(DataSequence.get_words()))
    return sorted(sequences)