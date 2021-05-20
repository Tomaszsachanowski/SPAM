#!/usr/bin/env python3


"""Definicja klasy Singleton i podstawowej konfiguracji"""


class Singleton(type):
    """Metaklasa ze wzorem Singletonu"""
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class Config(metaclass=Singleton):
    TWEET = {
        'CONSUMER_KEY': '4Aq6KSNh7oke2DVWIFuq4Vdae',
        'CONSUMER_SECRET': 'TRu8Y9ZYystbQs6biF8KR3DRM8k1GbTRnsZQNuKAuhamjl1Zl8',
        'ACCESS_TOKEN': '1392905688318361603-k7lYPGzirhJpqhYd8RCDdQt4cW8jVE',
        'ACCESS_SECRET': 's4lwFsSPrdJN2qWCmqlUrnA5DpHcf95XXlNpFAM16fN7U',
        'search_word': "#Covid-19",
        'items': 10,
        'output': 'data/tweet_output.csv',
        'customers': 'name',
        'texts': 'text'
    }

    TEST = {
        "path": "./data/test_data.csv",
        "customers": "name",
        "texts": "text"
    }
