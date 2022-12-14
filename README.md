# transferable_biomarkers

This is a repo for the transferable biomarkers from cell lines to patients which are associated with drug response

## System Requirements and Packages
* Operating Systems Linux (CentOS version 7 and Ubuntu 20.04 LTS)
* Python versions=3.9
* Pandas versions=1.3.5
* Numpy versions=1.21.5
* Scikit-learn=0.24.2
* XGBoost versions=1.5.0
* Scipy versions=1.7.3
* Keras version=2.7.0

## Large files to download
1- download "proae.hdf5" https://drive.google.com/file/d/1BuHTzLuq8dhd90ETQGEkbd7zh1uamIty/view?usp=sharing to "model" folder.

2- download "sanger-dose-response.csv" https://drive.google.com/file/d/1cngLTLCUv7mpQU2K4nEkmlZAcYA9fZYB/view?usp=sharing to "data" folder.

3- download "CCLE_expression.csv" https://drive.google.com/file/d/1wwRE7c9k9MuvA7dYCRAAhkmv2ju9ZTvR/view?usp=sharing to "data" folder.

4- download "tcga_norm_count_1.csv" https://drive.google.com/file/d/1ymY78HIQXz-RbqJUFVTA1x5g7o2ZhYNa/view?usp=sharing to "data" folder.

5- download "tcga_norm_count_2.csv" https://drive.google.com/file/d/1b0NnPwWgG2gdH7Vb4n4SeTNLUcnRCB_X/view?usp=sharing to "data" folder.



## Extract genes from cell lines correlate with drug response

To extract genes correlate with drug response in cell lines, run the following command

```python src/extract_genes_cell_lines.py```

## Extract Genes from Patients which correlate with drug response by calculating C-Index

Genes that are correlated with drug response in cell lines, are then checked in TCGA, the following command extract genes that also are correlated with drug response in patients

```python src/calculate_cindex.py```

## Generate gene embedding using trained covolutional autoencoder

In order to extract/generate gene embedding using its sequence, run the following command

```python src/generate_embedding.py```

## Train and Evaluate Classifiers

1- Download the training data set "full_train_data.csv" to train model https://drive.google.com/file/d/1SsWGrc_RrBeeiRrtz4bUFiAtxNrjPWB9/view?usp=sharing and save it in "model" folder

2- Download the test data set "full_test_data.csv" to evaluate classifiers https://drive.google.com/file/d/1baXAcZHQ2-EFbDNm-2-66HGUUagu0hFw/view?usp=sharing and save it in "model" folder

3- Run ```python model/train.py``` to train and evaluate the performance of both classifiers Random Forest and XGBoost

