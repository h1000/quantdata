# -*- coding:utf-8 -*-
from quantdata.db.mongo import Mongo
from datetime import datetime
from quantdata import logger
import pandas as pd


mongo = Mongo()
db = mongo.getDB()

#set log 
LOGGER_NAME = "get the PB"
mylog = logger.getLogger(LOGGER_NAME)
#get the stocklist 
stock_list = db.stock_list.find()

for row in stock_list:
    ticker = str(row['ticker'])
    mylog.info("processing %s"%(ticker))
    stock_hist_list = db.cn_stock_hist.find({"ticker":ticker})
    hist_list = []
    for stock_row in stock_hist_list:
        tradDate = datetime.strptime(stock_row['tradeDate'],"%Y-%m-%d")
        if stock_row['PE'] <= 0 or stock_row['PB'] <= 0:
            continue
        hist_list.append({'date':stock_row['tradeDate'],'pb':stock_row['PB'],'pe':stock_row['PE'],'year':tradDate.year})
    
    df = pd.DataFrame(hist_list)
    df = df.dropna()
    group = df.groupby("year")
    df2 = group.min()
    df2.to_csv("/home/jacob/pe/%s.csv"%(ticker))
#get the lowest pe year by year 

#make all year lowest pe pb into a dataframe 

#store dataframe to a csv


