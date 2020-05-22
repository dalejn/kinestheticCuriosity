source activate evoAlg

for file in `ls testFit_*.py`
do
    python $file
done