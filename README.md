# CSVv2ScikitLearn
Repository for scripts to prepare the trees and for executing the scikit-learn version of the CSVv2 training

STEPS:

1) Skimming trees: 

root -l Filter_ttjets.C

root -l Filter_qcd.C


2) Compute yields:

python compute_yields.py qcd

python compute_yields.py ttjets


3) Compute weights:

python compute_weights.py


4) Add weightBranch to training trees

python addWeightBranch.py qcd --apply-pteta-weight --apply-category-weight --apply-flavour-weight


5) Execute training (first setup the right environment for scikit-learn: https://github.com/smoortga/iihe_sklearn_tutorial)

python sklearn_training_GBT.py
