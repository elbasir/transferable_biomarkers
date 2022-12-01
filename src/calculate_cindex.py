import pandas as pd
from sksurv.metrics import concordance_index_censored

def get_data(gene, drug_col):
    df = pd.read_csv("data/full_clean_TCGA.csv", usecols=[drug_col, gene])
    df = df.dropna()
    cindex = []
    drugs = df['pa_drug'].tolist()
    gene_data = df[gene].tolist()
    for i in range(len(drugs)):
        drugs[i] = drugs[i].split(',')[1]

    for i in range(len(drugs)):
        drugs[i] = drugs[i].split('.')[0]

    unique_drug = list(set(drugs))

    for i in range(len(unique_drug)):
        data = []
        for j in range(len(drugs)):
            if(unique_drug[i] == drugs[j]):
                data.append(gene_data[j])
        if(len(data) > 1):
            ci = calculate_cindex(data, unique_drug[i], gene)
            cindex.append(ci)
    if(len(cindex) > 0):
        return(cindex)
    else:
        return(False)

def calculate_cindex(data, drug, gene):
    #f1 = pd.DataFrame(data)
    #f1 = f1.dropna()
    #data = f1.values.tolist()
    gene_exp = []
    os_time = []
    os = []
    for i in range(len(data)):
        _row = data[i].split(',')
        gene_exp.append(float(_row[1]))
        os_time.append(float(_row[2]))
        os.append(bool(float(_row[3])))
    t = []
    t.append(gene)
    t.append(drug)
    if(len(os) > 1):
        try:
            c = concordance_index_censored(os, os_time, gene_exp)
            t.append(c[0])
        except:
            t.append("All samples are censored")
    if(len(t) > 0):
        return(t)
    else:
        retun(['NaN', 'NaN', 'NaN'])


for ch in pd.read_csv("data/full_clean_TCGA.csv", chunksize=1):
    break
    
genecols = ch.columns[1:]
drugcol = ch.columns[0]

cindex  = []
for gene in genecols:
    ci = get_data(gene, drugcol)
    if(ci != False):
        for i in range(len(ci)):
            cindex.append(ci[i])

df = pd.DataFrame(cindex)
df.columns = ['Gene_name', 'Drug_name', 'CI']
#df.to_csv("CI_gene_drug_May_13.csv", index=False)
df.to_csv("output/gene_drug_CIndex.csv", index=False)
