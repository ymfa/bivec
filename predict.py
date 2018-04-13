#!/usr/bin/env python3
import sys
import numpy as np
from scipy.spatial.distance import cosine

if len(sys.argv) < 4:
  print("Usage: ./predict.py SCEmbed TCEmbed WindowSize")
  sys.exit()
sc_model, tc_model = sys.argv[1], sys.argv[2]
window_size = int(sys.argv[3])

from gensim.models import KeyedVectors
sc_vectors = KeyedVectors.load_word2vec_format(sc_model, binary=False)
tc_vectors = KeyedVectors.load_word2vec_format(tc_model, binary=False)

print('Input format: Sentence Position Candidates')
print('Example: 工程干了好多天 2 幹乾干')

while True:
  try:
    query = input('>>> ')
    sentence, pos, candidates = query.split()
  except (ValueError, EOFError): break
  idx = int(pos)
  context = sentence[max(0,idx-window_size):idx] + sentence[idx+1:idx+window_size+1]
  context_vectors = [sc_vectors[c] if c in sc_vectors else sc_vectors['<unk>'] for c in context]
  context_vector = np.average(context_vectors, axis=0)
  results = []
  for candidate in candidates:
    if candidate not in tc_vectors: continue
    candidate_vector = tc_vectors[candidate]
    sim = 1. - cosine(context_vector, candidate_vector)
    results.append((sim, candidate))
  for sim, char in sorted(results, reverse=True):
    print(' *  %s %f' % (char, sim))
