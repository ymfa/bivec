#!/usr/bin/env python3
import sys, re
from collections import Counter

if len(sys.argv) < 3:
  print("Usage: ./make_data.py InputPrefix OutputPrefix [VocabSize]")
  print("Input files are under corpora/; output files are under data/.")
  sys.exit()
prefix = sys.argv[1]
in_prefix = 'corpora/' + prefix
out_prefix = 'data/' + prefix

if len(sys.argv) > 2:
  dict_size = int(sys.argv[2])
else:
  dict_size = None  # unlimited vocab

# Character ranges according to https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
# Some codepoints in these ranges are not currently in use
non_hz = re.compile(r'[^\u3400-\u4DBF\u4E00-\u9FFF\U00020000-\U0002A6DF\U0002A700-\U0002B73F\U0002B740-\U0002B81F\U0002B820-\U0002CEAF\U0002CEB0-\U0002EBEF\uF900-\uFAFF\U0002F800-\U0002FA1F]+')

def filter_hz(s, vocab):
  return ' '.join(c if c in vocab else '<unk>' for c in s)

def process_file(fin, fout):
  # collect sentences and build vocab
  sentences = []
  if dict_size: vocab = Counter()
  for sentence in fin:
    sentence = non_hz.sub('', sentence)
    if sentence:
      if dict_size: vocab.update(sentence)
      sentences.append(sentence)
  if dict_size: vocab = set(k for k, v in vocab.most_common(dict_size))
  # write file
  for sentence in sentences:
    if dict_size: sentence = filter_hz(sentence, vocab)
    else: sentence = ' '.join(sentence)
    fout.write(sentence + '\n')
  return [len(s) for s in sentences]

with open(in_prefix + '.tc', 'r') as fin:
  with open(out_prefix + '.de', 'w') as fout:
    tc_counts = process_file(fin, fout)

with open(in_prefix + '.sc', 'r') as fin:
  with open(out_prefix + '.en', 'w') as fout:
    sc_counts = process_file(fin, fout)

if tc_counts != sc_counts:
  print('Error: Input lengths do not match.')
  sys.exit()

with open(out_prefix + '.de-en', 'w') as fout:
  for tc_len in tc_counts:
    fout.write(' '.join('%d %d' % (x, x) for x in range(tc_len)) + '\n')