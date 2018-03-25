from quantdata.analyze import AbstractAnalyze
from quantdata.stock import quotes
from quantdata import logger
from quantdata.util.func import *
import pandas as pd
import numpy as np
import os
import json
import xlwt


class GuaidianJsonV2Analyze(AbstractAnalyze):

    def __init__(self):
        self.__logger = logger.getLogger("GuaidianJson")
        self.__data_path = './stockdata/mainreport'
        self.__choose_stock = {}

    def get_code_list(self):
        try:
            stock_list = quotes.get_stock_hq_list()
            return stock_list["code"].tolist()
        except Exception as e:
            self.__logger.error("get code list error:%s"%(e))
            return []

    def __get_main_report_df(self,code):

        with open(os.path.join(self.__data_path,code+".json"),"r") as f:
            report_obj = json.load(f)
            colums  = [x[0] if isinstance(x, list) else x for x in report_obj['title']]
            df = pd.DataFrame(columns=colums)
            for i in range(0,len(colums)):
                df[colums[i]] = report_obj["report"][i]
            df = df.set_index(colums[0])
            df = df.sort_index(ascending=True)
            return df

    def analyze_data(self,code):
        try:
            '''寻找业绩拐点，业绩拐点波幅为50%'''
            df = self.__get_main_report_df(code)
            margin_incr_series = df['净利润同比增长率']
            margin_pivots = num_peak_valley_pivots(margin_incr_series,50,-50)
            if margin_pivots is None or margin_pivots[-1] != 1 or margin_incr_series[-1] == '' or self._to_float(margin_incr_series[-1]) < -10:
                return False,"code:%s,pivots:%s"%(code,margin_incr_series.tolist())
            for i in range(-2,-5,-1):
                #在长度范围或4季度内
                if abs(i) > len(margin_pivots) or abs(i) > 4:
                    return False,{"code":code,"margin_incr_series":margin_incr_series,"margin_pivots":margin_pivots}
                elif margin_pivots[i] == 1:
                    return False, {"code":code,"margin_incr_series":margin_incr_series,"margin_pivots":margin_pivots}
                elif margin_pivots[i] == -1:
                    return True,{"code":code,"margin_incr_series":margin_incr_series,"margin_pivots":margin_pivots}
            return False,{"code":code,"margin_incr_series":margin_incr_series,"margin_pivots":margin_pivots}
        except Exception as e:
            self.__logger.error("analyze error:%s"%(e))
            return False,{"code":code}

    def _to_float(self, num):
        try:
            return float(num)
        except:
            return 0.0

    def store_success_result(self,data):
        if data is not None and "code" in data:
            self.__choose_stock[data['code']] = data

    def store_fail_result(self,data):
        if data is not None:
            pass


    def write_execl(self):
        wb = xlwt.Workbook()
        sheet = wb.add_sheet("业绩拐点")
        code_list = self.__choose_stock.keys()
        for i, code in enumerate(code_list):
            sheet.write(i,0,code)
            sheet.write(i,1,str(self.__choose_stock[code]['margin_incr_series'].tolist()[-10:]))
            sheet.write(i,2, str(self.__choose_stock[code]['margin_pivots'].tolist()[-10:]))
        wb.save("./chosestock.xls")


if __name__ == "__main__":
    ana = GuaidianJsonV2Analyze()
    ana.run(100)
    ana.write_execl()
