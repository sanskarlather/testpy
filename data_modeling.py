from cgi import test
from re import T

import matplotlib.pyplot as mp
import numpy as n
import pandas as p
import seaborn as s
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

data_U=p.read_csv('urldata.csv')

# ─── DATA PREPROCESSING ─────────────────────────────────────────────────────────

print("Description of the data")
print(data_U.describe())#Description of the entire data to figure out basic info about the data
data_S = data_U.drop(['Domain'], axis = 1).copy()
print(data_S.isnull().sum())#Null value checker
data_S=data_S.sample(frac=1).reset_index(drop=True)#Randomizing rows so as to avoid over fitting

# ─── DATA SPLITTING ─────────────────────────────────────────────────────────────
y=data_S['Label']
x=data_S.drop('Label',axis=1)#Sepration of features and targets
print(x.shape,y.shape)
#Splitting in training and testing
X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                    test_size = 0.2, random_state = 12)
print("Training and testing data")
print(X_train.shape, X_test.shape)

#
# ────────────────────────────────────────────────────────────────────── I ──────────
#   :::::: T R A I N I N G   M O D E L S : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────────────────────────
#

# ─── STORING THE RESULTS ────────────────────────────────────────────────────────
model_ML=[]
train_R=[]
test_R=[]
def result_S(model,a,b):
    model_ML.append(model)
    train_R.append(round(a,4))
    test_R.append(round(b,4))


# ─── DECISION TREE ───────────────────────────────────────────────────────────────
tree_D=DecisionTreeClassifier(max_depth=5)
tree_D.fit(X_train, y_train)
y_test_tree = tree_D.predict(X_test)
y_train_tree = tree_D.predict(X_train)
tree_train_R=accuracy_score(y_train,y_train_tree)
tree_test_R=accuracy_score(y_test,y_test_tree)

print("Decision Tree: Accuracy on training Data: {:.3f}".format(tree_train_R))
print("Decision Tree: Accuracy on test Data: {:.3f}".format(tree_test_R))
result_S('Random Forest', tree_train_R, tree_test_R)


# ─── RANDOM FOREST CLASSIFER ────────────────────────────────────────────────────
forest_R=RandomForestClassifier(max_depth=5)
forest_R.fit(X_train, y_train)
y_test_forest=forest_R.predict(X_test)
y_train_forest=forest_R.predict(X_train)
forest_train_R=accuracy_score(y_train,y_train_forest)
forest_test_R=accuracy_score(y_test,y_test_forest)

print("Random forest: Accuracy on training Data: {:.3f}".format(forest_train_R))
print("Random forest: Accuracy on test Data: {:.3f}".format(forest_test_R))
result_S('Random Forest', forest_train_R, forest_test_R)

# ─── DEEP LEARNING ──────────────────────────────────────────────────────────────
model_DL=MLPClassifier(alpha=0.001, hidden_layer_sizes=([100,100,100]))
model_DL.fit(X_train,y_train)
y_test_mlp = model_DL.predict(X_test)
y_train_mlp = model_DL.predict(X_train)
DL_train_R=accuracy_score(y_train,y_train_mlp)
DL_test_R=accuracy_score(y_test,y_test_mlp)

print("Deep Learning: Accuracy on training Data: {:.3f}".format(DL_train_R))
print("Deep Learning: Accuracy on test Data: {:.3f}".format(DL_test_R))
result_S('Deep Learning', DL_train_R,DL_test_R)

# ─── XGBOOST ────────────────────────────────────────────────────────────────────
model_XG=XGBClassifier(learning_rate=0.4,max_depth=7)
model_XG.fit(X_train,y_train)
y_test_xgb = model_XG.predict(X_test)
y_train_xgb = model_XG.predict(X_train)
XGB_train_R=accuracy_score(y_train,y_train_xgb)
XGB_testa_R= accuracy_score(y_test,y_test_xgb)
print("XGBoost: Accuracy on training Data: {:.3f}".format(XGB_train_R))
print("XGBoost : Accuracy on test Data: {:.3f}".format(XGB_testa_R))
result_S('XGBoost', XGB_train_R,XGB_testa_R)

# ─── SVC ────────────────────────────────────────────────────────────────────────
model_SV=SVC(kernel='linear', C=1.0, random_state=12)
model_SV.fit(X_train,y_train)
y_test_svm=model_SV.predict(X_test)
y_train_svm=model_SV.predict(X_train)
SVM_train_R=accuracy_score(y_train,y_train_svm)
SVM_test_R=accuracy_score(y_test,y_test_svm)
print("SVM: Accuracy on training Data: {:.3f}".format(SVM_train_R))
print("SVM : Accuracy on test Data: {:.3f}".format(SVM_test_R))
result_S('SVM', SVM_train_R,SVM_test_R)

results = p.DataFrame({ 'ML Model': model_ML,    
    'Train Accuracy': train_R,
    'Test Accuracy': test_R})
print(results.sort_values(by=['Test Accuracy', 'Train Accuracy'], ascending=False))
