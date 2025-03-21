import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
#import seaborn as sns  

Chla=pd.read_excel('path/Rationality analysis data.xlsx', sheet_name = 'night') #day and night
Chla.info()
Chla.dropna(inplace=True)
enc = LabelEncoder()
enc.fit(Chla['name']) 
Chla['name'] = enc.transform(Chla['name']) +1
enc.fit(Chla['lake']) 
Chla['lake'] = enc.transform(Chla['lake'])+1  

X=Chla.iloc[:,np.r_[1:13]]
y=Chla['chla']
#test and train
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                    test_size=0.3, random_state=123)
y_test = np.log10(y_test)
y_train = np.log10(y_train)
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error,r2_score, make_scorer
scoring = {'rmse': make_scorer(mean_squared_error),
            'r2':make_scorer(r2_score)}     
param_grid = {#'criterion': ['squared_error', 'absolute_error'],
              'n_estimators': [25,50, 100, 200], 
              'max_depth': [ 8, 9, 10, 11, 12], 
              'min_samples_split': [3, 4, 5, 6]} 
dtr = RandomForestRegressor ()
dtrcv = GridSearchCV (estimator=dtr, param_grid=param_grid, 
                      scoring=scoring,refit='r2',cv=5,n_jobs=10) 
dtrcv.fit(X_train,y_train)   
train_result = dtrcv.predict(X_train)
test_result = dtrcv.predict(X_test)
dtrcv.best_params_
def scores(predictions, targets):
    rmse=mean_squared_error(predictions, targets)
    r2=r2_score(predictions, targets)
    nse=(1-(sum((predictions-targets)**2)/sum((targets-np.mean(targets))**2)))
    return {'Models': 'RandomForestRegressor','rmse': rmse, 'r2': r2,'nse': nse}
train_scores = pd.DataFrame((scores(y_train, train_result)),index=['0',])
test_scores = pd.DataFrame((scores(y_test, test_result)),index=['0',])

from sklearn.inspection import permutation_importance

train_importance = permutation_importance(dtrcv, X_train, y_train,scoring='neg_mean_squared_error', n_repeats=100,
                                random_state=42, n_jobs=-1)
sorted_idx = train_importance.importances_mean.argsort()

fig, ax = plt.subplots()
ax.boxplot(train_importance.importances[sorted_idx].T,
           vert=False, labels=X_train.columns[sorted_idx])
ax.set_title("Permutation Importances (train set)")
fig.tight_layout()
plt.show()

train_importance= pd.DataFrame(train_importance.importances[sorted_idx].T)
train_importance= train_importance.set_axis(X_train.columns[sorted_idx], axis='columns')


test_importance = permutation_importance(dtrcv, X_test, y_test,scoring='neg_mean_squared_error', n_repeats=100,
                                random_state=42, n_jobs=-1)
sorted_idx = test_importance.importances_mean.argsort()

fig, ax = plt.subplots()
ax.boxplot(test_importance.importances[sorted_idx].T,
           vert=False, labels=X_test.columns[sorted_idx])
ax.set_title("Permutation Importances (test set)")
fig.tight_layout()
plt.show()
test_importance= pd.DataFrame(test_importance.importances[sorted_idx].T)
test_importance= test_importance.set_axis(X_test.columns[sorted_idx], axis='columns')

train_result=pd.Series(train_result)
train_result.index=y_train.index

train_result=train_result.sort_index()
y_train=y_train.sort_index()


test_result=pd.Series(test_result)
test_result.index=y_test.index

test_result=test_result.sort_index()
y_test=y_test.sort_index()


def setlabel(ax, label, loc=2, borderpad=0.6, **kwargs):
    legend = ax.get_legend()
    if legend:
        ax.add_artist(legend)
    line, = ax.plot(np.NaN,np.NaN,color='none',label=label)
    label_legend = ax.legend(handles=[line],loc=loc,handlelength=0,handleheight=0,handletextpad=0,borderaxespad=0,borderpad=borderpad,frameon=False,**kwargs)
    label_legend.remove()
    ax.add_artist(label_legend)
    line.remove()
    
fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(7.5,4))
ax1.plot(y_train, label="True value", color='blue')
ax1.plot(train_result, label="Predict value",color='red')
ax1.set_title("training dataset")
ax1.set_xlabel("River temperature ($^\circ$C)") 
ax1.set_xlabel("Sample number") 
ax1.legend(loc='upper right')
setlabel(ax1, '(a)')

ax2.plot(y_test, label="True value", color='blue')
ax2.plot(test_result, label="Predict value",color='red')
ax2.set_title("testing dataset")
ax2.set_xlabel("River temperature ($^\circ$C)") 
ax2.set_xlabel("Sample number") 
ax2.legend(loc='upper right')
setlabel(ax2, '(b)')
fig.suptitle("RandomForestRegressor")
fig.tight_layout()
#plt.savefig('RandomForestRegressor.pdf') 

writer_orig = pd.ExcelWriter('Chla modelling results-RandomForestRegressor.xlsx', engine='xlsxwriter')
train_scores.to_excel(writer_orig, startrow = 0, startcol = 0, index=False, sheet_name='model evaluation')
test_scores.to_excel(writer_orig, startrow = 0, startcol = 5, index=False, sheet_name='model evaluation')

y_train.to_excel(writer_orig, startrow = 0, startcol = 0, index=True, sheet_name='training data')
train_result.to_excel(writer_orig, startrow = 0, startcol = 2, index=False, sheet_name='training data')

y_test.to_excel(writer_orig, startrow = 0, startcol = 0, index=True, sheet_name='testing data')
test_result.to_excel(writer_orig, startrow = 0, startcol = 2, index=False, sheet_name='testing data')


train_importance.to_excel(writer_orig, startrow = 0, startcol = 0, index=False, sheet_name='training importance')
test_importance.to_excel(writer_orig, startrow = 0, startcol = 0, index=False, sheet_name='testing importance')

writer_orig.save()