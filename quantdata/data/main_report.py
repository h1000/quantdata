from quantdata import logger
from quantdata.stock import quotes
from quantdata.db.mysql import Mysql
import time,json
from urllib.request import urlopen, Request
from quantdata import cons as ct
from pypinyin import lazy_pinyin
from quantdata.data import AbstractData


class MainReportToMysql(AbstractData):
    """
    更新基本报表数据到mysql数据库
    """
    def __init__(self):
        self.__logger = logger.getLogger("MainReportToMysql")
        self.__db = Mysql()
        self.__data = {}
        self.__zhongwen_2_pinyin = {}
        self.__pinyin_2_zhongwen = {}
        self.__db.add_table_not_exists("mainreport")
        self.__exists_colnums = self.__db.get_columns("mainreport")

    def get_code_list(self):
        try:
            stock_list = quotes.get_stock_hq_list()
            return stock_list["code"].tolist()
        except Exception as e:
            self.__logger.error(e)
            return []

    def check_update(self, code):
        db = Mysql()
        row = db.selectRow("select ke_mu_shi_jian from mainreport where code='%s' ORDER BY ke_mu_shi_jian DESC"%(code))
        if row is None or 'ke_mu_shi_jian' not in row:
            return True
        last_time = row['ke_mu_shi_jian']
        if code not in self.__data:
            self.__get_main_report_json(code)
        if code in self.__data:
            new_time = max(self.__data[code]['report'][0])
            if new_time > last_time:
                return True
            else:
                return False
        else:
            return False

    def update_data(self,code):
        """
        从同花顺获取股票基本面数据存入Mysql，对中文的列
        :param code:
        :return:
        """
        db = Mysql()
        self.__logger.info("update mainreport data of %s"%(code))
        #更新前先清除数据
        db.delete("mainreport",{"code":code})
        if code not in self.__data:
            self.__get_main_report_json(code)
        if code in self.__data and self.__data[code] is not None:
            self.__translate_title(self.__data[code]['title'])

            colnums = []
            for k, v in self.__pinyin_2_zhongwen.items():
                if k not in self.__exists_colnums:
                    self.__exists_colnums.append(k)
                    colnums.append({"name": k, "type": "varchar(100)", "comment": v})
            # 添加缺失的列到表中
            if len(colnums) > 0:
                db.add_columns("mainreport", colnums)
            # 处理report数据
            report = self.__data[code]['report']
            title = self.__data[code]['title']
            for j in range(0, len(report[0])):
                try:
                    data = {}
                    for i in range(0, len(report)):
                        if isinstance(title[i], str):
                            t = title[i]
                        elif isinstance(title[i], list):
                            t = title[i][0]
                        data[self.__zhongwen_2_pinyin[t]] = str(report[i][j])
                    data["code"] = code
                    self.__logger.debug("update mainreport data of %s:%s"%(code,data))
                    db.insert("mainreport", data)
                except Exception as e:
                    self.__logger.error("update error:%s,%s"%(code,e))
                    continue

    def __translate_title(self,title):
        for item in title:
            if isinstance(item, str):
                zhongwen = item
                if zhongwen in self.__zhongwen_2_pinyin:
                    continue
                else:
                    pinyin = "_".join(lazy_pinyin(zhongwen, errors='ignore'))
                    self.__pinyin_2_zhongwen[pinyin] = zhongwen
                    self.__zhongwen_2_pinyin[zhongwen] = pinyin
            elif isinstance(item, list):
                zhongwen = item[0]
                zhongwen2 = item[1]
                if zhongwen in self.__zhongwen_2_pinyin:
                    continue
                else:
                    pinyin = "_".join(lazy_pinyin(zhongwen, errors='ignore'))
                    self.__pinyin_2_zhongwen[pinyin] = zhongwen + "(" + zhongwen2 + ")"
                    self.__zhongwen_2_pinyin[zhongwen] = pinyin

    def __get_main_report_json(self,code):
        try:
            request = Request(ct.THS_MAIN_DATA_URL % (code))
            request.add_header("User-Agent", ct.USER_AGENT)
            text = urlopen(request, timeout=ct.API_TIMEOUT).read()
            text = text.decode('gbk') if ct.PY3 else text
            reportObj = json.loads(text.strip())
            if isinstance(reportObj, dict) and "title" in reportObj and "report" in reportObj:
                self.__data[code] = reportObj
            else:
                self.__data[code] = None
        except Exception as e:
            self.__logger.error(e)

if __name__ == "__main__":
    obj = MainReportToMysql()
    obj.run()






