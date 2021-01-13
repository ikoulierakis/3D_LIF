#!/bin/bash

seed=0
subject=SubjectAP_noscalp
number_of_layers=40
sigma=0.6
R=30

if test -f $subject\_$R\_$sigma.dat; then
echo "Connectivity Matrix Exists."
else
echo "$subject\_$R\_$sigma.dat does not exist..."
echo "Creating..."
python mri2matrix.py $subject/ $number_of_layers $sigma $R
fi

mkdir -p $seed $subject\_$R\_$sigma\_$seed/data/

echo ./3D_LIF $subject\_$R\_$sigma.dat $number_of_layers $seed $subject\_$R\_$sigma
export OMP_NUM_THREADS=4
time ./3D_LIF $subject\_$R\_$sigma.dat $number_of_layers $seed $subject\_$R\_$sigma
