#!/bin/bash

# read in arguments


usage() {
    echo  "$0: some help text"
}

inf='../test_cases/simp2multitrad_test'
config='s2tw'
seg_flag='
while [ "$1" != "" ]; do
    case $1 in
        -f | --input_filename )           shift
                                inf=$1
                                ;;
        -s | --segmentation)    shift
                                seg_flag=$1
                                ;;
        -c | --config)          shift
                                config=$1
                                ;;
                       
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit
    esac
    shift
done

filename=$(basename $inf)

outf=$filename'_opencc_'$config

#opencc
opencc -i $inf -o $outf -c ./OpenCC/data/config/$config.json 