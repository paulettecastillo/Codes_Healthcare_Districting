#!/bin/sh
## The second entry is multi-cut or uni-cut

# for beta in {0,0.3,0.5,0.7,1.0}
# do
beta=0
i=36
k=4
for j in {1..5}
do
taskset -c 0-1 python3 ./main.py ./Instances_${i}/Instances_${j}_${i}_10.txt ${k} ${beta} 1 1 1 DSF  > ./Salidas/Salida_${j}_${i}_SCFF2_S_${beta}_10_${k}
done


	





