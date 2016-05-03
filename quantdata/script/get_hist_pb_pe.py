# -*- coding:utf-8 -*-
from quantdata.db.mongo import Mongo
from datetime import datetime
from quantdata import logger
import pandas as pd


mongo = Mongo()
db = mongo.getDB()

#get the stocklist 
stock_list = db.stock_list.find()

for row in stock_list:
    ticker = str(row['ticker'])
    stock_hist = db.cn_stock_hist.find({"ticker":ticker})
    hist_list = []
    for stock_row in stock_list:
        tradDate = datetime.strptime(stock_row['tradeDate'],"%Y-%m-%d")
        hist_list.append({'date':stock_row['tradeDate'],'pb':stock_row['PB'],'pe':stock_row['PE'],'year':tradDate.year})
    
    df = pd.DataFrame(hist_list)
    group = df.groupby("year")
    print group
    break
#get the lowest pe year by year 

#make all year lowest pe pb into a dataframe 

#store dataframe to a csv


