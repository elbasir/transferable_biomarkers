# processing patient data
import pandas as pd

def process_survival_data():

    df = pd.read_csv("Survival_SupplementalTable_S1_20171025_xena_sp", on_bad_lines='skip', sep='\t')
    sample = df['sample'].tolist()
    patient = df['_PATIENT'].tolist()
    os_time = df['OS.time'].tolist()
    os = df['OS'].tolist()
    del df
    drug_dataframe = pd.read_csv("drug_tcga.csv")
    drug_name = drug_dataframe['drug_name'].tolist()
    bcr = drug_dataframe['bcr_patient_barcode'].tolist()
    survival_data = []
    for i in range(len(bcr)):
        for j in range(len(patient)):
            if(bcr[i] == patient[j]):
                tmp = []
                tmp.append(sample[j])
                tmp.append(patient[j])
                tmp.append(drug_name[i])
                tmp.append(os_time[j])
                tmp.append(os[j])
                survival_data.append(t)
    survival_data = pd.DataFrame(survival_data)
    survival_data.columns = ['sample', '_Patient', 'Drug_name', 'OS_time', 'OS']
    pcode = survival_data['sample'].tolist()
    patient = survival_data['_Patient'].tolist()
    drug_name = survival_data['Drug_name'].tolist()
    os_time = survival_data['OS_time'].tolist()
    os = survival_data['OS'].tolist()
    del survival_data
    
    return(pcode, patient, drug_name, os_time, os)



def get_exp_tcga(filename, pcode, patient, drug_name, os_time, os):
   
    df = pd.read_csv(filename)
    genes = df['sample'].tolist()
    cols = df.columns.tolist()
    tcga_dataframe = pd.DataFrame(index=range(len(genes)),columns=range(len(pcode)))
    
    for i in range(len(pcode)):
    data = []
    flag = 0
    for j in range(1, len(cols)):
        if(pcode[i] == cols[j]):
            flag = 1
            tcga_cols = df[cols[j]].tolist()
            for k in range(len(tcga_cols)):
                tmp = []
                tmp.append(patient[i])
                tmp.append(tcga_cols[k])
                tmp.append(float(os_time[i]))
                tmp.append(os[i])
                tmp = [str(i) for i in tmp]
                data.append(','.join(tmp))
        if(flag == 1):
            break
    if(len(data)>0):
        tcga_dataframe[i] = data
    
    
    del df
    pdcols = []
    for i in range(len(pcode)):
        tmp = []
        tmp.append(pcode[i])
        tmp.append(drug_name[i])
        pdcols.append(','.join(tmp))
    tcga_dataframe.index = genes
    tcga_dataframe.columns = pdcols
    
    return tcga_dataframe

pcode, patient, drug_name, os_time, os = process_survival_data()
tcga_dataframe_1 = get_exp_tcga(filename='tcga_norm_count_1.csv', pcode, patient, drug_name, os_time, os)
tcga_dataframe_2 = get_exp_tcga(filename='tcga_norm_count_2.csv', pcode, patient, drug_name, os_time, os)
tcga_dataframe = [tcga_dataframe_1, tcga_dataframe_2]
tcga_dataframe = pd.contact(tcga_dataframe)
tcga_dataframe = tcga_dataframe.T
tcga_dataframe.columns = tcga_dataframe.iloc[0].tolist()
tcga_dataframe = tcga_dataframe.iloc[1:]
tcga_dataframe = tcga_dataframe.rename(columns={'Unnamed: 0': 'pa_drug'})
tcga_dataframe.to_csv("full_clean_TCGA.csv", index=False)
