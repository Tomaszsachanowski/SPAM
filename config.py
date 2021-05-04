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
    TEST = {
        "path": "./data/test_data.csv",
        "customers": "country",
        "texts": "description"
    }