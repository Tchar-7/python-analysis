import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation,LabelSpreading
from sklearn.model_selection import train_test_split
from sklearn import metrics 
from sklearn.metrics import confusion_matrix 
from sklearn.decomposition import PCA
import joblib

def load_data():
    stone  = pd.read_excel("stone.xlsx")
    skill = pd.read_excel("skill.xlsx")
    #处理缺失值
    stone.fillna({"二技能":"无","Lv1":0},inplace=True)
    #处理技能,将技能名称用数字替换
    skillArray = skill["LookUpName"].values
    stone['一技能'].replace(skillArray,list(range(1,113)),inplace=True)
    stone['二技能'].replace(skillArray,list(range(1,113)),inplace=True)

    pca = PCA(n_components=1)
    skill1=stone[['一技能','Lv']]
    re_1=pca.fit_transform(skill1)
    skill2=stone[['二技能','Lv1']]
    re_2=pca.fit_transform(skill2)
    totalskill=np.concatenate((re_1,re_2),axis=1)
    re_skill=pca.fit_transform(totalskill)
    re_skill
    stone = pd.concat((stone,pd.DataFrame(re_skill)),axis = 1)
    # stone = pd.concat((stone,pd.DataFrame(re_2)),axis = 1)
    # stone.drop(['一技能','Lv','二技能','Lv1'],axis = 1,inplace=True)
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
        if i > 500:
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
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    alphas=np.linspace(0.01,0.99,num=10,endpoint=True)
    gammas=np.logspace(-2,2,num=50)
    colors=((1,0,0),(0,1,0),(0,0,1),(0.5,0.5,0),(0,0.5,0.5),
        (0.5,0,0.5),(0.4,0.6,0),(0.6,0.4,0),(0,0.6,0.4),(0.5,0.3,0.2),)
    #训练并绘图
    for alpha,color in zip(alphas,colors):
        scores=[]
        for gamma in gammas:
            clf=LabelSpreading(max_iter=100,gamma=gamma,
                alpha=alpha,kernel='rbf')
            clf.fit(X,Y_train)
            predicted_labels=clf.transduction_[unlabeled_index]
            scores.append(metrics.accuracy_score(Y[unlabeled_index],predicted_labels))
        ax.plot(gammas,scores,label=r"$\alpha=%s$"%alpha,color=color)

    #设置图形
    ax.set_xlabel(r'$\gamma$')
    ax.set_ylabel('score')
    ax.set_xscale('log')
    ax.legend(loc='best')
    ax.set_title('LabelSpreading rbf kernel')
    plt.show()

    # cls=LabelSpreading(max_iter=100,kernel='rbf',gamma=0.76,alpha=0.7722)
    # cls.fit(X,Y_train)
    # predicted_labels=cls.transduction_[unlabeled_index]
    # Y_train[unlabeled_index] = predicted_labels

    # pd.DataFrame(Y_train).to_excel("./new2.xlsx")
    # print("Accuracy:%f"%metrics.accuracy_score(Y[unlabeled_index],predicted_labels))

    # joblib.dump(cls, 'cls.model')
    # spread = joblib.load('cls.model')



X,Y,unlabeled_index=load_data()
#test_LabelPropagation(X,Y,unlabeled_index)
test_LabelSpreading(X,Y,unlabeled_index)


# from sklearn.externals import joblib
# #lr是一个LogisticRegression模型
# joblib.dump(lr, 'lr.model')
# lr = joblib.load('lr.model')

