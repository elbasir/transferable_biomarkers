# transferable_biomarkers

This is a repo for the transferable biomarkers from cell lines to patients which are associated with better drug response

#### Large files to download
1- download "proae.hdf5" https://drive.google.com/file/d/1BuHTzLuq8dhd90ETQGEkbd7zh1uamIty/view?usp=sharing to "model" folder.

2- download "sanger-dose-response.csv" https://drive.google.com/file/d/1cngLTLCUv7mpQU2K4nEkmlZAcYA9fZYB/view?usp=sharing to "data" folder.

3- download "CCLE_expression.csv" https://drive.google.com/file/d/1wwRE7c9k9MuvA7dYCRAAhkmv2ju9ZTvR/view?usp=sharing to "data" folder.

4- download "tcga_norm_count_1.csv" https://drive.google.com/file/d/1ymY78HIQXz-RbqJUFVTA1x5g7o2ZhYNa/view?usp=sharing to "data" folder.

5- download "tcga_norm_count_2.csv" https://drive.google.com/file/d/1b0NnPwWgG2gdH7Vb4n4SeTNLUcnRCB_X/view?usp=sharing to "data" folder.

#### Train and Evaluate Classifiers

1- Download full data set to train model "gene_drug_full_dataset.csv" https://drive.google.com/file/d/1rQ78s9aRSHGZoXA5hM3TxNBD0DLdG-ga/view?usp=sharing and save it in "model" folder

2- Run ```python model/train.py``` to train and evaluate the performance of both classifiers Random Forest and XGBoost

