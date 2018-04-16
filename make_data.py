#!/usr/bin/env python3
import sys, re
from collections import Counter

if len(sys.argv) < 3:
  print("Usage: ./make_data.py FileNamePrefix [MinFreq]")
  print("I will look for input files under corpora/, output files under data/.")
  print("i.e. input files are corpora/FileNamePrefix.sc and corpora/FileNamePrefix.tc.")
  sys.exit()
prefix = sys.argv[1]
in_prefix = 'corpora/' + prefix
out_prefix = 'data/' + prefix

if len(sys.argv) > 2:
  min_freq = int(sys.argv[2])
else:
  min_freq = 0  # unlimited vocab

# Character ranges according to https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
# Some codepoints in these ranges are not currently in use
non_hz = re.compile(r'[^\u3400-\u4DBF\u4E00-\u9FFF\U00020000-\U0002A6DF\U0002A700-\U0002B73F\U0002B740-\U0002B81F\U0002B820-\U0002CEAF\U0002CEB0-\U0002EBEF\uF900-\uFAFF\U0002F800-\U0002FA1F]+')

def filter_hz(s, vocab):
  return ' '.join(c if c in vocab else '<unk>' for c in s)

def process_file(fin, fout):
  # collect sentences and build vocab
  sentences = []
  if min_freq: vocab = Counter()
  for sentence in fin:
    sentence = non_hz.sub('', sentence)
    if sentence:
      if min_freq: vocab.update(sentence)
      sentences.append(sentence)
  if min_freq:
    vocab = set(k for k, v in vocab.items() if v >= min_freq)
    print('vocab size:', len(vocab))
  # write file
  for sentence in sentences:
    if min_freq: sentence = filter_hz(sentence, vocab)
    else: sentence = ' '.join(sentence)
    fout.write(sentence + '\n')
  return [len(s) for s in sentences]

with open(in_prefix + '.tc', 'r') as fin:
  with open(out_prefix + '.de', 'w') as fout:
    print('TC', end=' ')
    tc_counts = process_file(fin, fout)

with open(in_prefix + '.sc', 'r') as fin:
  with open(out_prefix + '.en', 'w') as fout:
    print('SC', end=' ')
    sc_counts = process_file(fin, fout)

if tc_counts != sc_counts:
  print('Error: Input lengths do not match.')
  sys.exit()

with open(out_prefix + '.de-en', 'w') as fout:
  for tc_len in tc_counts:
    fout.write(' '.join('%d %d' % (x, x) for x in range(tc_len)) + '\n')