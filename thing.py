

# ONLY USE THIS BLOCK OF CODE ON NICASIA'S COMPUTER 
import sys
sys.path.append("/anaconda/lib/python2.7/site-packages")
#####


import pandas as pd
import numpy as np
from matplotlib.patches import Polygon
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler as Standardize
from sklearn.linear_model import LinearRegression as Lin_Reg
from sklearn.linear_model import Ridge as Ridge_Reg
from sklearn.linear_model import Lasso as Lasso_Reg
from sklearn.preprocessing import PolynomialFeatures
from sklearn import ensemble
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.regression.linear_model import OLS
import string
import matplotlib.pyplot as plt
#%matplotlib inline
import math


train = pd.read_csv("train_imputed.csv")
test = pd.read_csv("test_imputed.csv")


x_train = train.drop(['zestimate_amount'], 1)
y_train = train['zestimate_amount']
x_test = test.drop(['zestimate_amount'], 1)
y_test = test['zestimate_amount']


#--------  k_fold_r_squared
# A function for k-fold cross validation with Ridge regression
# Input: 
#      x_train (n x d array of predictors in training data)
#      y_train (n x 1 array of response variable vals in training data)
#      num_folds (no. of folds for CV)
#      param_val (regularization parameter value)
# Return: 
#      average R^2 value across folds

def k_fold_r_squared(x_train, y_train, num_folds):
    n_train = x_train.shape[0]
    n = int(np.round(n_train * 1. / num_folds)) # points per fold

    # Iterate over folds
    cv_r_squared = 0
    
    for fold in range(1, num_folds + 1):
        # Take k-1 folds for training 
        x_first_half = x_train.iloc[:n * (fold - 1), :]
        x_second_half = x_train.iloc[n * fold + 1:, :]
        x_train_cv = np.concatenate((x_first_half, x_second_half), axis=0)
        
        y_first_half = y_train.iloc[:n * (fold - 1)]
        y_second_half = y_train.iloc[n * fold + 1:]
        y_train_cv = np.concatenate((y_first_half, y_second_half), axis=0)
        
        # Take the middle fold for testing
        x_test_cv = x_train.iloc[1 + n * (fold - 1):n * fold, :]
        y_test_cv = y_train.iloc[1 + n * (fold - 1):n * fold]

        # Fit ridge regression model with parameter value on CV train set, and evaluate CV test performance
        reg = Pipeline([('poly', PolynomialFeatures(degree=3)), ('linear', Lin_Reg(fit_intercept=False))])
        reg.fit(x_train_cv, y_train_cv)
        r_squared = reg.score(x_test_cv, y_test_cv)
    
        # Cummulative R^2 value across folds
        cv_r_squared += r_squared

    # Return average R^2 value across folds
    return cv_r_squared * 1.0 / num_folds


k_fold_r_squared(x_train, y_train, 5)


reg = Pipeline([('poly', PolynomialFeatures(degree=3)), ('linear', Lin_Reg(fit_intercept=False))])
reg.fit(x_train, y_train)
r_squared = reg.score(x_test, y_test)

# Best CV parameter value
best_cv_param = np.argmax(cv_r_squared)

# Print R^2 for best CV parameter, max R^2 across all parameters, and R^2 for plain regression
print 'Polynomial regression: Test R^2 score for CV choice', test_r_squared[best_cv_param]
print 'Polynomial regression: Max Test R^2 score', max(test_r_squared)
print 'Polynomial regression: Test R^2 score:', test_r_squared_plain
