import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from matplotlib import gridspec
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, matthews_corrcoef
from sklearn.metrics import confusion_matrix
data=pd.read_csv("creditcard.csv")
X=data.drop(['Class'], axis=1)
Y=data["Class"]
xData=X.values
yData=Y.values
xTrain, xTest, yTrain, yTest = train_test_split(xData, yData, test_size = 0.2, random_state = 42)
rfc = RandomForestClassifier()
rfc = joblib.load('random_forest_model.joblib')
yPred = rfc.predict(xTest)
fraud = data[data['Class'] == 1]
n_outliers = len(fraud)
n_errors = (yPred != yTest).sum()
print("The model used is Random Forest classifier")
acc = accuracy_score(yTest, yPred)
print(f"The accuracy is {acc}")
prec = precision_score(yTest, yPred)
print(f"The precision is {prec}")
rec = recall_score(yTest, yPred)
cv=5
print(f"The recall is {rec}")
f1 = f1_score(yTest, yPred)
print(f"The F1-Score is {f1}")
MCC = matthews_corrcoef(yTest, yPred)
print(f"The Matthews correlation coefficient is{MCC}")
