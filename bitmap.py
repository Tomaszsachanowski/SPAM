import numpy as np

class seq_bitmap():

    def __init__(self, seq, bitmap):
        self.seq = seq
        self.bitmap = bitmap

    def get_bitmap(self):
        return self.bitmap