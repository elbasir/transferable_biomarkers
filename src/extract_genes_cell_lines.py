# script to extract genes correlate with drug response in cell lines
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.utils import shuffle
np.random.seed(423)

def extact_gene_name_exp():
    
    '''extracts the gene expression Cell lines'''
    ccle_df = pd.read_csv("CCLE_expression.csv")
    celline = list(ccle_df['Unnamed: 0'])
    ccle_df = ccle_df.rename(columns={i: i.split(' ')[0] for i in list(ccle_df.columns)})
    tmp_df = ccle_df.loc[:, 'TSPAN6':'AC113348.1']
    gene_exp = tmp_df.values.tolist()

    return(tmp_df.columns.tolist(), gene_exp, celline)

def extract_drug_cline_data():
    
    '''extracts drugs in cell lines with their IC50 values'''
    
    drug_df = pd.read_csv("sanger-dose-response.csv")
    drug_df = drug_df[drug_df['DRUG_NAME'].notna()]
    drug_df = drug_df[drug_df['IC50_PUBLISHED'].notna()]
    ic50_published = drug_df['IC50_PUBLISHED'].tolist()
    cline = drug_df['ARXSPAN_ID'].tolist()
    drugs = drug_df['DRUG_NAME'].tolist()
    broad_id = drug_df['BROAD_ID'].tolist()
    ec50 = drug_df['ec50'].tolist()
    dataset = drug_df['DATASET'].tolist()
    d1 = {(cline[i],drugs[i]):ic50_published[i] for i in range(len(dataset)) if dataset[i]=='GDSC1'}
    d2 = {(cline[i], drugs[i]): ic50_published[i] for i in range(len(dataset)) if dataset[i] == 'GDSC2'}

    cell_drug_pair = []
    
    for i in range(len(drugs)):
        cell_drug_pair.append((cline[i],drugs[i]))

    unique_p = list(set(cell_drug_pair))

    dict_selected={}
    for i in range(len(unique_p)):
        if unique_p[i] in d1 and unique_p[i] in d2:
            dict_selected[unique_p[i]]=min(d1[unique_p[i]],d2[unique_p[i]])
        elif unique_p[i] in d1:
            dict_selected[unique_p[i]] = d1[unique_p[i]]
        else:
            dict_selected[unique_p[i]] = d2[unique_p[i]]

    return(list(dict_selected.values()), [i[1] for i in list(dict_selected.keys())], [i[0] for i in list(dict_selected.keys())])

def collect_data(gene_exp, celline, ic50, drug, cline):
    
    data = []
    for i in range(len(cline)):
        for j in range(len(gene_exp)):
            if(cline[i] == celline[j]):
                tmp = []
                tmp.append(cline[i])
                tmp.append(drug[i])
                tmp.append(ic50[i])
                for k in range(len(gene_exp[j])):
                    tmp.append(gene_exp[j][k])
                data.append(tmp)
                
    return data


def filtering_func(drug, drugs, ic50, cellines):

    selected_ic50 = []
    selected_drugs = []
    selected_cline = []
    for i in range(len(drug)):
        for j in range(len(drugs)):
            if(drug[i] == drugs[j]):
                selected_ic50.append(ic50[j])
                selected_drugs.append(drugs[j])
                selected_cline.append(cellines[j])

    return(selected_ic50, selected_drugs, selected_cline)



def correlation_func(df_data, drug, gene_names):

    corr_data = []
    max_corr = 0
    for i in range(len(drug)):
        for j in range(len(gene_names)):
            df_tmp = df_data[['IC50', gene_names[j]]].where(df_data['Drug_name'] == drug[i]).dropna()
            tmp_corr = (spearmanr(df_tmp['IC50'], df_tmp[gene_names[j]])[0])
            corr_data.append((drug[i], gene_names[j], spearmanr(df_data['IC50'], df_data[gene_names[j]], nan_policy='omit')[0], spearmanr(df_data['IC50'], df_data[gene_names[j]],nan_policy='omit')[1]))
            if(tmp_corr > max_corr):
                max_corr = tmp_corr

    return pd.DataFrame(corr_data)

gene_names, gene_exp,celline=extact_gene_name_exp()

ic50,drugs,cellines=extract_drug_cline_data()

drugs = shuffle(drugs)

drug = []
for i in range(80):
    drug.append(drugs[i])

ic50, drugs, cellines = filtering_func(drug, drugs, ic50, cellines)


data = collect_data(gene_exp, celline,ic50, drugs, cellines)

df_data = pd.DataFrame(data)

cols = ['Cell_line', 'Drug_name', 'IC50']

for i in range(len(gene_names)):
    cols.append(gene_names[i])

df_data.columns = cols

del data, gene_exp, celline,ic50, drugs, cellines

drug = list(set(df_data['Drug_name'].tolist()))

corr_data = correlation_func(df_data, drug, gene_names)
corr_data.columns = ['Drug_name', 'Gene_name', 'correlation_coff', 'P-value']

## Filter gene-drug correlation by correlation coefficient > 0.1 and P-value < 0.05 ##
corr_data = corr_data[corr_data['correlation_coff'] > 0.1]
corr_data = corr_data[corr_data['P-value'] < 0.05]

corr_data.to_csv("gene_drug_correlation_coff.csv", index=False)
print("Drug Gene Correlation Coff table is saved...")
