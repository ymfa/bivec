#!/usr/bin/env python3
import sys, re
from collections import Counter

if len(sys.argv) < 2:
  print("Usage: ./make_data.py FileNamePrefix [MinFreq]")
  print("I will look for input files under corpora/, output files under data/.")
  print("i.e. input files are corpora/FileNamePrefix.sc and corpora/FileNamePrefix.tc.")
  sys.exit()
prefix = sys.argv[1]
in_prefix = 'corpora/' + prefix
out_prefix = 'data/' + prefix
section_size = 1000000


if len(sys.argv) > 2:
  min_freq = int(sys.argv[2])
else:
  min_freq = 0  # unlimited vocab

whitespce = re.compile(r'\s+')
numeric = re.compile(r'(\d+[\d．.－\-]*\d+|\d)')
basic_latin = re.compile(r'([{l}]+[{l}－\-]*[{l}]+|[{l}])'.format(l='A-Za-zＡ-Ｚａ-ｚ'))

def filter_char(s):
  s = whitespce.sub('', s)
  s = numeric.sub('0', s)
  s = basic_latin.sub('A', s)
  return s

def filter_vocab(s, vocab):
  return ' '.join(c if c in vocab else '<unk>' for c in s)

def process_file(fin, fout):
  # collect sentences and build vocab
  sentences = []
  max_num_tokens = 0
  if min_freq: vocab = Counter()
  for i, sentence in enumerate(fin):
    if i % section_size == 0: print('.', end='', flush=True)
    sentence = filter_char(sentence)
    if sentence:
      if min_freq: vocab.update(sentence)
      sentences.append(sentence)
      max_num_tokens = max(max_num_tokens, len(sentence))
  if min_freq:
    vocab = set(k for k, v in vocab.items() if v >= min_freq)
    print('vocab size:', len(vocab), end='')
  # write file
  for i, sentence in enumerate(sentences):
    if i % section_size == 0: print('.', end='', flush=True)
    if min_freq: sentence = filter_vocab(sentence, vocab)
    else: sentence = ' '.join(sentence)
    fout.write(sentence + '\n')
  print('longest line: ', max_num_tokens)
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

  for i, tc_len in enumerate(tc_counts):
    if i % section_size == 0: print('.', end='', flush=True)
    fout.write(' '.join('%d %d' % (x, x) for x in range(tc_len)) + '\n')
  print()
