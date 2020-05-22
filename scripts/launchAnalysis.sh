#!/bin/bash
#$ -binding linear:10
#$ -pe unihost 10
#$ -S /bin/bash
#$ -cwd

source activate evoAlg
cd /scripts

for file in `ls nsga_*.py`
do
    python -m scoop -vv $file
done