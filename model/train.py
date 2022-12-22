import pandas as pd
import random
import numpy as np
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix precision_score, recall_score, f1_score, accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

train_data = pd.read_csv("full_train_data.csv")
X_train = []
y_train = []
for i in range(len(train_data)):
    X_train.append(train_data.iloc[i][2:-1].tolist())
    y_train.append(train_data.iloc[i][-1])
    
test_data = pd.read_csv("full_test_data.csv")

X_test = []
y_test = []
for i in range(len(test_data)):
    X_test.append(test_data.iloc[i][2:-1].tolist())
    y_test.append(test_data.iloc[i][-1])
    
X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)
y_test = np.array(y_test)

### Random Forest Classifier###
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

### XGBoost Classifier###

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
