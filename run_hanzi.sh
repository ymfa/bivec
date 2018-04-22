#!/usr/bin/env bash

if [[ $# -lt 4 ]]; then
  echo "Usage: `basename $0` trainPrefix dim win threads"
  echo "  trainPrefix: Path to training files excluding extensions"
  echo "  dim: Number of vector dimensions"
  echo "  win: Context window size"
  echo "  threads: Number of CPU threads"
  exit
fi

trainPrefix=$1
dim=$2
win=$3
threads=$4
logfile=run_hanzi.$(date -u +'%m%d%H%M%S').log

if [ ! -d "embeddings" ]; then
  mkdir embeddings
fi


command="./bivec -src-train ${trainPrefix}.de -tgt-train ${trainPrefix}.en -size ${dim} \
        -src-lang de -tgt-lang en -align ${trainPrefix}.de-en -align-opt 1 \
        -output embeddings/out-$win-$dim -cbow 0 -window ${win} -negative 10 \
        -threads ${threads} -iter 30"


echo "time ${command}" &> ${logfile}
time ${command} &>> ${logfile}
