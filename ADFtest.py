import operator
import numpy as np
import statsmodels.tsa.stattools as sts
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import statsmodels.api as sm
from datetime import datetime
from scipy.stats.stats import pearsonr
Rank = {}

potentialPair =[['601818', '601328'], ['601818', '601988'], ['601328', '600036'], ['600036', '601166'], ['601328', '601988'], ['601818', '600036'], ['601328', '601166'], ['601818', '601166']]
for i in range(len(potentialPair)):
    m = str(potentialPair[i][0])
    n = str(potentialPair[i][1])
    price_of_1 = ts.get_hist_data(m, start='2016-01-01', end='2016-12-01').iloc[::-1]
    price_of_2 = ts.get_hist_data(n, start='2016-01-01', end='2016-12-01').iloc[::-1]
    price_of_1 = price_of_1.dropna()
    price_of_2 = price_of_2.dropna()
    closeprice_of_1 = pd.DataFrame(price_of_1['close']/price_of_1['close'][0])
    closeprice_of_2 = pd.DataFrame(price_of_2['close']/price_of_2['close'][0])
    close_price_final = pd.merge(closeprice_of_1, closeprice_of_2, left_index=True, right_index=True)
    if len(closeprice_of_1) != 0 and len(closeprice_of_2) != 0:
        model = pd.ols(y=close_price_final['close_y'], x=close_price_final['close_x'], intercept=True)   # perform ols on these two stocks
        #print(model.beta)
        spread = close_price_final['close_y'] - close_price_final['close_x']*model.beta['x']#.beta-只取x变量前系数
        sta = sts.adfuller(spread, 1)
        print(sta)
        pair = m + '+' + n
        Rank[pair] = sta[0]#Augmented Dickey-Fuller test 拒绝域{u<u0},代表平稳，H0为序列不平稳
        rank2 = sorted(Rank.items(), key=operator.itemgetter(1))
        #print(rank2)
        #spread.plot()
        b = model.beta['intercept']
        k = model.beta['x']
        x = [0.8, 1.2]
        y = [0.8*k + b, 1.2*k + b]
        df = pd.DataFrame(x, y)
        df.plot(xlim=[0.75, 1.2], ylim=[0.8, 1.05])#plot fitting line
        plt.scatter(close_price_final['close_y'].values, close_price_final['close_x'].values)
        plt.show()

