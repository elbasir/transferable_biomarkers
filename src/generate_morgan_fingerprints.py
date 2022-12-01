import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem


# If you do not have RDKit package installed, you can check RDKit documentation at: https://www.rdkit.org/docs/Install.html
# approved drug names ##
drug_name = ['BICALUTAMIDE', 'EPIRUBICIN', 'BLEOMYCIN', 'VINCRISTINE', 'SORAFENIB', 'ETOPOSIDE', 'CYCLOPHOSPHAMIDE', 'METHOTREXATE', 'TAMOXIFEN', 'VINBLASTINE']


# Canonical smiles for approved drugs 
smiles = ['CC(CS(=O)(=O)C1=CC=C(C=C1)F)(C(=O)NC2=CC(=C(C=C2)C#N)C(F)(F)F)O', 'CC1C(C(CC(O1)OC2CC(CC3=C2C(=C4C(=C3O)C(=O)C5=C(C4=O)C(=CC=C5)OC)O)(C(=O)CO)O)N)O', 'CC1=C(N=C(N=C1N)C(CC(=O)N)NCC(C(=O)N)N)C(=O)NC(C(C2=CN=CN2)OC3C(C(C(C(O3)CO)O)O)OC4C(C(C(C(O4)CO)O)OC(=O)N)O)C(=O)NC(C)C(C(C)C(=O)NC(C(C)O)C(=O)NCCC5=NC(=CS5)C6=NC(=CS6)C(=O)NCCC[S+](C)C)O', 'CCC1(CC2CC(C3=C(CCN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)C78CCN9C7C(C=CC9)(C(C(C8N6C=O)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC)O', 'CNC(=O)C1=NC=CC(=C1)OC2=CC=C(C=C2)NC(=O)NC3=CC(=C(C=C3)Cl)C(F)(F)F', 'CC1OCC2C(O1)C(C(C(O2)OC3C4COC(=O)C4C(C5=CC6=C(C=C35)OCO6)C7=CC(=C(C(=C7)OC)O)OC)O)O', 'C1CNP(=O)(OC1)N(CCCl)CCCl', 'CN(CC1=CN=C2C(=N1)C(=NC(=N2)N)N)C3=CC=C(C=C3)C(=O)NC(CCC(=O)O)C(=O)O', 'CCC(=C(C1=CC=CC=C1)C2=CC=C(C=C2)OCCN(C)C)C3=CC=CC=C3', 'CCC1(CC2CC(C3=C(CCN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)C78CCN9C7C(C=CC9)(C(C(C8N6C)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC)O'] 

def generate_mfp(drugs, smiles):
    # Generating Morgan Fingerprints for each drug using its canonical smiles ##
    morgan_fp = []
    for i in range(len(smiles)):
        mol = Chem.MolFromSmiles(smiles[i])
        fps = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
        tmp = []
        tmp.append(drugs[i])
        for f in fps:
            tmp.append(f)
        morgan_fp.append(tmp)
    return(morgan_fp)


morgan_fp = generate_mfp(drug_name, smiles)
