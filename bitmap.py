import numpy as np
from math import ceil

from read_data import generate_simple_sequeneces




sequences = generate_simple_sequeneces()



def generate_words_bitmaps(sequences):
    lenght_of_unique_word = len(sequences[0].get_words())
    cids = sequences[0].get_customers().values()
    counts = dict(zip(cids, [0]*len(cids)))
    bit_vectors_for_cid = dict()

    for s in sequences:
        bit_vector = np.zeros(lenght_of_unique_word)
        bit_vector[s.unique_words_ids] = [1]*len(s.unique_words_ids)
        bit_vectors_for_cid.setdefault(s.cid, []).append(bit_vector)
        counts[s.cid] = counts[s.cid] + 1

    maximum = max(counts.values())
    k = 2**(ceil(maximum/2))

    all_vectors = []
    for cid in cids:
        bit_vector = np.zeros(lenght_of_unique_word)
        bit_vectors = [bit_vector]*(k - counts[cid])
        all_vectors.extend(bit_vectors)
        all_vectors.extend(bit_vectors_for_cid[cid])

    all_bitmap = np.array(all_vectors)
    print(all_bitmap)

    bit_vectors_for_word_ids = dict()
    for column in range(lenght_of_unique_word):
        column_vector = all_bitmap[:,column]
        column_vector_splited = np.split(column_vector, len(cids))
        bit_vectors_for_word_ids[column] = column_vector_splited

    return bit_vectors_for_word_ids

bitmaps_for_words_ids = generate_words_bitmaps(sequences)
print(bitmaps_for_words_ids)