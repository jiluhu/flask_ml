#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 导入类库
import numpy as np
from numpy import arange
from matplotlib import pyplot
from pandas import read_csv
from pandas import  set_option
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error

# 导入数据
# 导入数据
filename = 'data/housing.csv'
names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS',
         'RAD', 'TAX', 'PRTATIO', 'B', 'LSTAT', 'MEDV']
dataset = read_csv(filename, names=names, delim_whitespace=True)

# 通过表格方式显示数据基本信息
def showInfo(dataset):
    # 数据维度
    print(dataset.shape)

    # 特征熟悉的字段类型
    print(dataset.dtypes)

    # 查看最开始的30条记录
    set_option('display.line_width', 120)
    print(dataset.head(30))

    # 描述性统计信息
    set_option('precision', 1)
    print(dataset.describe())

    # 关联关系
    set_option('precision', 2)
    print(dataset.corr(method='pearson'))



# 通过直方图、密度图、箱线图和散点矩阵度对数据有个全方位的了解
def showGraph(dataset):

    # 直方图
    dataset.hist(sharex=False, sharey=False, xlabelsize=1, ylabelsize=1)
    pyplot.show()

    # 密度图
    dataset.plot(kind='density', subplots=True, layout=(4, 4), sharex=False, fontsize=1)
    pyplot.show()

    # 箱线图
    dataset.plot(kind='box', subplots=True, layout=(4, 4), sharex=False, sharey=False, fontsize=8)
    pyplot.show()

    # 散点矩阵图
    scatter_matrix(dataset)
    pyplot.show()

    # 相关矩阵图
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(dataset.corr(), vmin=-1, vmax=1, interpolation='none')
    fig.colorbar(cax)
    ticks = np.arange(0, 14, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)
    pyplot.show()


# 算法比较
def compareAlgorithm(X_train,Y_train,X_validation,Y_validation, num_folds=10, seed=7, scoring='neg_mean_squared_error'):



    # 评估算法 - baseline
    models = {}
    models['LR'] = LinearRegression()
    models['LASSO'] = Lasso()
    models['EN'] = ElasticNet()
    models['KNN'] = KNeighborsRegressor()
    models['CART'] = DecisionTreeRegressor()
    models['SVM'] = SVR()

    # 评估算法
    results = []
    for key in models:
        kfold = KFold(n_splits=num_folds, random_state=seed)
        cv_result = cross_val_score(models[key], X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_result)
        print('%s: %f (%f)' % (key, cv_result.mean(), cv_result.std()))

# compareAlgorithm(dataset, 13, 0.2, 10, 7, 'neg_mean_squared_error')


def compareAlgorithm_Pipelines(X_train,Y_train,X_validation,Y_validation, num_folds=10, seed=7, scoring='neg_mean_squared_error'):


    # 评估算法 - 正态化数据
    pipelines = {}
    pipelines['ScalerLR'] = Pipeline([('Scaler', StandardScaler()), ('LR', LinearRegression())])
    pipelines['ScalerLASSO'] = Pipeline([('Scaler', StandardScaler()), ('LASSO', Lasso())])
    pipelines['ScalerEN'] = Pipeline([('Scaler', StandardScaler()), ('EN', ElasticNet())])
    pipelines['ScalerKNN'] = Pipeline([('Scaler', StandardScaler()), ('KNN', KNeighborsRegressor())])
    pipelines['ScalerCART'] = Pipeline([('Scaler', StandardScaler()), ('CART', DecisionTreeRegressor())])
    pipelines['ScalerSVM'] = Pipeline([('Scaler', StandardScaler()), ('SVM', SVR())])
    results = []
    for key in pipelines:
        kfold = KFold(n_splits=num_folds, random_state=seed)
        cv_result = cross_val_score(pipelines[key], X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_result)
        print('%s: %f (%f)' % (key, cv_result.mean(), cv_result.std()))

    return pipelines, results

# compareAlgorithm_Pipelines(dataset, 13, 0.2, 10, 7, 'neg_mean_squared_error')

def compareAlgorithm_Ensemble(X_train,Y_train,X_validation,Y_validation, num_folds=10, seed=7, scoring='neg_mean_squared_error'):

    # 集成算法
    ensembles = {}
    ensembles['ScaledAB'] = Pipeline([('Scaler', StandardScaler()), ('AB', AdaBoostRegressor())])
    ensembles['ScaledAB-KNN'] = Pipeline([('Scaler', StandardScaler()),
                                          ('ABKNN',
                                           AdaBoostRegressor(base_estimator=KNeighborsRegressor(n_neighbors=3)))])
    ensembles['ScaledAB-LR'] = Pipeline([('Scaler', StandardScaler()), ('ABLR', AdaBoostRegressor(LinearRegression()))])
    ensembles['ScaledRFR'] = Pipeline([('Scaler', StandardScaler()), ('RFR', RandomForestRegressor())])
    ensembles['ScaledETR'] = Pipeline([('Scaler', StandardScaler()), ('ETR', ExtraTreesRegressor())])
    ensembles['ScaledGBR'] = Pipeline([('Scaler', StandardScaler()), ('RBR', GradientBoostingRegressor())])

    results = []
    for key in ensembles:
        kfold = KFold(n_splits=num_folds, random_state=seed)
        cv_result = cross_val_score(ensembles[key], X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_result)
        print('%s: %f (%f)' % (key, cv_result.mean(), cv_result.std()))
    return ensembles, results

# compareAlgorithm_Ensemble(dataset, 13, 0.2, 10, 7, 'neg_mean_squared_error')

def compareAlgorithm_BoxLine(models, results):
    # 箱线图比较算法
    fig = pyplot.figure()
    fig.suptitle('Algorithm Comparison')
    ax = fig.add_subplot(111)
    pyplot.boxplot(results)
    ax.set_xticklabels(models.keys())
    pyplot.show()

# models, results = compareAlgorithm_Ensemble(dataset, 13, 0.2, 10, 7, 'neg_mean_squared_error')
# compareAlgorithm_BoxLine(models, results)

# K近邻算法的K值默认是5个，可以通过网格搜索算法优化参数
def optimizeAlgorithm_KNN(X_train,Y_train,X_validation,Y_validation, num_folds=10, seed=7, scoring='neg_mean_squared_error'):


    # 调参改进算法 - KNN
    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    param_grid = {'n_neighbors': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]}
    model = KNeighborsRegressor()
    kfold = KFold(n_splits=num_folds, random_state=seed)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
    grid_result = grid.fit(X=rescaledX, y=Y_train)

    print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))
    cv_results = zip(grid_result.cv_results_['mean_test_score'],
                     grid_result.cv_results_['std_test_score'],
                     grid_result.cv_results_['params'])
    for mean, std, param in cv_results:
        print('%f (%f) with %r' % (mean, std, param))

# optimizeAlgorithm_KNN(dataset, 13, validationSizeRatio=0.2, num_folds=10, seed= 7, scoring='neg_mean_squared_error')

# 集成算法GBM - 调参
def optimizeAlgorithm_GradientBoosting(X_train,Y_train,X_validation,Y_validation, num_folds=10, seed=7, scoring='neg_mean_squared_error'):

    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    param_grid = {'n_estimators': [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900]}
    model = GradientBoostingRegressor()
    kfold = KFold(n_splits=num_folds, random_state=seed)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
    grid_result = grid.fit(X=rescaledX, y=Y_train)
    print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))

# optimizeAlgorithm_GradientBoosting(dataset, 13, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='neg_mean_squared_error')

    # 集成算法ET - 调参
def optimizeAlgorithm_ExtraTrees(X_train,Y_train,X_validation,Y_validation, num_folds=10, seed=7, scoring='neg_mean_squared_error'):

    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    param_grid = {'n_estimators': [5, 10, 20, 30, 40, 50, 60, 70, 80]}
    model = ExtraTreesRegressor()
    kfold = KFold(n_splits=num_folds, random_state=seed)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
    grid_result = grid.fit(X=rescaledX, y=Y_train)

    print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))

# optimizeAlgorithm_ExtraTrees(dataset, 13, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='neg_mean_squared_error')

def algorithm_ExtraTrees(X_train,Y_train,X_validation,Y_validation, seed=7):


    # 训练模型
    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    gbr = ExtraTreesRegressor(n_estimators=80)
    gbr.fit(X=rescaledX, y=Y_train)
    # 评估算法模型
    rescaledX_validation = scaler.transform(X_validation)
    predictions = gbr.predict(rescaledX_validation)
    print(mean_squared_error(Y_validation, predictions))

algorithm_ExtraTrees(dataset, 13)
