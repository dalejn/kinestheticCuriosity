#!/bin/bash

paste indexList.txt scriptList2.txt | while IFS="$(printf '\t')" read -r f1 f2
do
    printf 'sed -i "s#subjectNumber = 0#subjectNumber = %s#g" %s\n' "$f1" "$f2" >> editCommands
done
