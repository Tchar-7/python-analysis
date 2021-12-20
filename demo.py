import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation,LabelSpreading
from sklearn.linear_model import LogisticRegression 
from sklearn import svm 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.naive_bayes import GaussianNB 
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics 
from sklearn.metrics import confusion_matrix 

def load_data():
    stone  = pd.read_excel("stone.xlsx")
    skill = pd.read_excel("skill.xlsx")
#    处理缺失值
    stone.fillna({"二技能":"无","Lv.1":0},inplace=True)

#处理技能,将技能名称用数字替换
    skillArray = skill["LookUpName"].values
    stone['一技能'].replace(skillArray,list(range(1,114)),inplace=True)
    stone['二技能'].replace(skillArray,list(range(1,114)),inplace=True)

    target = 'value'
    x_columns=[x for x in stone.columns if x not in [target]]
    X = stone[x_columns]
    Y = stone['value']
    print(X)
    # x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.4)
    # x_train.shape,y_train.shape,x_test.shape,y_test.shape
    index = []
    # print(y_train.shape[0])
    for i in range(Y.shape[0]):
        # print(Y[i])
        if Y[i] == -1:
            index.append(i)
    return X,Y,index

def test_LabelPropagation(*data):
    X,Y,unlabeled_index=data
    Y_train=np.copy(Y)
    Y_train[unlabeled_index]=-1
    cls=LabelPropagation(max_iter=100,kernel='rbf',gamma=0.1)
    cls.fit(X,Y_train)
    print("Accuracy:%f"%cls.score(X[unlabeled_index],Y[unlabeled_index]))

def test_LabelSpreading(*data):
    X,Y,unlabeled_index=data
    Y_train=np.copy(Y)
    Y_train[unlabeled_index]=-1
    cls=LabelSpreading(max_iter=100,kernel='rbf',gamma=0.1)
    cls.fit(X,Y_train)
    predicted_labels=cls.transduction_[unlabeled_index]

    sum = 0
    for i in predicted_labels:
        sum +=1
        # print(i)
    Y[unlabeled_index] = predicted_labels
    print(Y)
    # print(predicted_labels)

    # print(sum)
    print(pd.concat([X,Y]))
    Y.to_excel("./new.xlsx")
    # print("Accuracy:%f"%metrics.accuracy_score(true_labels,predicted_labels))

X,Y,unlabeled_index=load_data()
#test_LabelPropagation(X,Y,unlabeled_index)
test_LabelSpreading(X,Y,unlabeled_index)
