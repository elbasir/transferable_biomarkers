import pandas as pd

import numpy as np
from sklearn.utils import shuffle
import sklearn.metrics as metrics
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

final_data = pd.read_csv("gene_drug_full_dataset.csv")
tmp_data = final_data.values.tolist()

X_data = []
y_data = []
for i in range(len(tmp_data)):
    tmp1 = tmp_data[i][3:3+1024]
    tmp2 = tmp_data[i][-65:-1]
    X_data.append(np.concatenate([tmp1, tmp2]))
    #X_train.append(tmp_data[i][2307:-1])
    y_data.append(tmp_data[i][-1])
    
gene = final_data['Gene_name'].tolist()
drug = final_data['Drug_name'].tolist()


filtered_genes = []
filtered_drugs = []
features = []
labels = []

for i in range(len(drug)):
    
    # Excluding hormone therapy drugs
    if(drug[i] != 'BICALUTAMIDE' and drug[i]!='TAMOXIFEN'):
        features.append(X_data[i])
        labels.append(y_data[i])
        filtered_drugs.append(drug[i])
        filtered_genes.append(gene[i])
        
X_train, X_test, y_train, y_test, drug_train, drug_test, gene_train, gene_test = train_test_split(features, labels,
                                                                                filtered_drugs, filtered_genes, test_size=0.15, random_state=17, stratify=filtered_drugs)


X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

### Random Forest Model
n_estimators = 40
max_depth = 3
#np.random.seed(42)
clf = RandomForestClassifier(max_depth=max_depth,n_estimators=n_estimators, random_state=13)
clf.fit(X_train, y_train)
y_pred = clf.predict_proba(X_test)[:,1]
pred = clf.predict(X_test)
  
auc = roc_auc_score(y_test, y_pred)
acc = accuracy_score(y_test, pred)
recall = recall_score(y_test, pred)
precision = precision_score(y_test, pred)
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
specific = tn / (tn+fp)
f1 = f1_score(y_test, pred)

print("Accuracy: %.2f%%" % (acc * 100.0))
print("AUC: %.2f%%" % (auc *100.0))
print("Recall: %.2f%%" % (recall*100.0))
print("Precision: %.2f%%" % (precision*100.0))
print("Specificity: %.2f%%" % (specific*100.0))
print("F1: %.2f%%" % (f1*100.0))

# XGBoost model with best hyper parameters

params = {
'max_depth':9,
'min_child_weight':8,
'eta':0.1,
'subsample':0.6,
'colsample_bytree':0.6,
'objective':'binary:logistic'
}
clf = xgb.XGBClassifier(**params)
clf.fit(X_train, y_train)
y_pred = clf.predict_proba(X_test)[:,1]
pred = clf.predict(X_test)
  
auc = roc_auc_score(y_test, y_pred)
acc = accuracy_score(y_test, pred)
recall = recall_score(y_test, pred)
precision = precision_score(y_test, pred)
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
specific = tn / (tn+fp)
f1 = f1_score(y_test, pred)

print("Accuracy: %.2f%%" % (acc * 100.0))
print("AUC: %.2f%%" % (auc *100.0))
print("Recall: %.2f%%" % (recall*100.0))
print("Precision: %.2f%%" % (precision*100.0))
print("Specificity: %.2f%%" % (specific*100.0))
print("F1: %.2f%%" % (f1*100.0))
