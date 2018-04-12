#!/usr/bin/env bash

if [[ $# -lt 2 ]]; then
  echo "Usage: `basename $0` trainPrefix dim"
  echo "  trainPrefix: Path to training files excluding extensions"
  echo "  dim: Number of vector dimensions"
  exit
fi

trainPrefix=$1
dim=$2

if [ ! -d "embeddings" ]; then
  mkdir embeddings
fi

./bivec -src-train $trainPrefix.de -tgt-train $trainPrefix.en -size $dim \
        -src-lang de -tgt-lang en -align $trainPrefix.de-en -align-opt 1 \
        -output embeddings/out -cbow 0 -window 5 -negative 10 \
        -threads 8 -iter 5
