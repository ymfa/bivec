#!/bin/bash

for file in ./cna_cmn/*; do
  echo $file 
  sed -i '1i <root>' "$file" &&
  echo '</root>' >> "$file"
done
