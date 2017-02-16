import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd

potentialPair = [['601818', '601328'], ['601818', '601988'], ['601328', '600036'], ['600036', '601166'], ['601328', '601988'], ['601818', '600036'], ['601328', '601166'], ['601818', '601166']]

for i in range(len(potentialPair)):
    m = str(potentialPair[i][0])
    n = str(potentialPair[i][1])
    price_of_1 = ts.get_hist_data(m, start='2016-01-01', end='2016-12-01').iloc[::-1].dropna()
    price_of_2 = ts.get_hist_data(n, start='2016-01-01', end='2016-12-01').iloc[::-1].dropna()
    closeprice_of_1 = pd.DataFrame(price_of_1['close']/price_of_1['close'][0])
    closeprice_of_2 = pd.DataFrame(price_of_2['close']/price_of_2['close'][0])

    close_price_final = pd.merge(closeprice_of_1,  closeprice_of_2, left_index=True, right_index=True)
    print(len(close_price_final))
    plt.show(close_price_final.plot())



