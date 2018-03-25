from quantdata.data import AbstractData
from quantdata.stock import quotes
from quantdata import logger
from urllib.request import urlopen, Request
from quantdata import cons as ct

import json
import os


class MainReportJson(AbstractData):


    def __init__(self):

        self.__logger = logger.getLogger("MainReportJson")
        self.__data_path = './stockdata/mainreport'
        if not os.path.exists(self.__data_path):
            os.makedirs(self.__data_path)

    def check_update(self,code):
        """直接覆盖文件"""
        return  True

    def get_code_list(self):
        try:
            stock_list = quotes.get_stock_hq_list()
            return stock_list["code"].tolist()
        except Exception as e:
            self.__logger.error(e)
            return []

    def update_data(self, code):
        self.__logger.info("update mainreport data of %s" % (code))
        reportObj = self.__get_main_report_json(code)
        if reportObj is None:
            return None
        with open(os.path.join(self.__data_path,code + ".json"),"w") as f:
            json.dump(reportObj,f)

    def __get_main_report_json(self,code):
        try:
            request = Request(ct.THS_MAIN_DATA_URL % (code))
            request.add_header("User-Agent", ct.USER_AGENT)
            text = urlopen(request, timeout=ct.API_TIMEOUT).read()
            text = text.decode('gbk') if ct.PY3 else text
            reportObj = json.loads(text.strip())
            if isinstance(reportObj, dict) and "title" in reportObj and "report" in reportObj:
                return reportObj
            else:
                return None
        except Exception as e:
            self.__logger.error(e)

if __name__ == "__main__":
    obj = MainReportJson()
    obj.run()
