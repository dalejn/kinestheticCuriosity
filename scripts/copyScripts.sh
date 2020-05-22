#!/bin/bash

paste scriptList.txt | while IFS="$(printf '\t')" read -r f1
do
  printf 'cp nsga.py nsga_%s.py\n' "$f1" >> copyCommands
done