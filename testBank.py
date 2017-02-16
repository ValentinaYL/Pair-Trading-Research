import operator
import numpy as np
import tushare as ts
import pandas as pd
stockPool = ['601818', '601998', '601169', '002142', '601398', '601328', '600000', '601288', '601939', '600036', '000001', '600016', '601988', '601166']
rank = {}
Rank = {}
for i in range(14):
    for j in range(i+1, 14):
        if i != j:
            # get the price of stock from TuShare
            price_of_i = ts.get_hist_data(stockPool[i], start='2016-01-01', end='2016-12-01').iloc[::-1].dropna()
            price_of_j = ts.get_hist_data(stockPool[j], start='2016-01-01', end='2016-12-01').iloc[::-1].dropna()
            closePrice_of_ij = pd.concat([price_of_i['close'], price_of_j['close']], axis=1)
            closePrice_of_ij = closePrice_of_ij.dropna()#去掉缺失值
            # change the column name in the dataFrame
            closePrice_of_ij.columns = ['close_i', 'close_j']
            # calculate the daily return and drop the return of first day cause it is NaN.计算每日回报
            ret_of_i = ((closePrice_of_ij['close_i'] - closePrice_of_ij['close_i'].shift())/closePrice_of_ij['close_i'].shift()).dropna()
            ret_of_j = ((closePrice_of_ij['close_j'] - closePrice_of_ij['close_j'].shift())/closePrice_of_ij['close_j'].shift()).dropna()
            # calculate the correlation and store them in rank1
            if len(ret_of_i) == len(ret_of_j):
                correlation = np.corrcoef(ret_of_i.tolist(), ret_of_j.tolist())#计算每日回报的相关系数,求出的是矩阵，用correlation[0, 1]取出相关系数
                m = stockPool[i] + '+' + stockPool[j]
                rank[m] = correlation[0, 1]
    rank1 = sorted(rank.items(), key=operator.itemgetter(1))#排序 sorted(列表名，key = operator.iteemgetter(1)即根据第二个域排序 )
    print(rank1)
    potentialPair = [list(map(str, item[0].split('+'))) for item in rank1]
    potentialPair = potentialPair[-8:]#取最大的8对
potentialPair.reverse()
print(potentialPair)