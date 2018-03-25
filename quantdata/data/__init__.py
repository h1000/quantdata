from abc import ABCMeta, abstractmethod
import threading,time

class AbstractData(object):
    __metaclass__  = ABCMeta

    @abstractmethod
    def check_update(self,code):
        """
        检查当前代码的数据是否要更新
        :param code:
        :return: Boolean
        """
        raise NotImplementedError("Should implement check_update()")

    @abstractmethod
    def get_code_list(self):
        """
        返回要获取数据的代码列表
        :return: list
        """
        raise NotImplementedError("Should implement get_code_list()")

    @abstractmethod
    def update_data(self,code):
        """
        更新某代码的数据
        :param code:
        :return:
        """
        raise NotImplementedError("Should implement update_data()")

    def batch_fetch_data(self,code_list):
        """
        批量获取数据
        :param code_list:
        :return:
        """
        for code in code_list:
            if self.check_update(code):
                #休息一秒,防止抓数据太快被封了IP
                time.sleep(1)
                self.update_data(code)



    def run(self,thread_num = 100):
        """
        多线程并发获取数据
        :return:
        """
        code_list = self.get_code_list()
        all_code_list = [code_list[i:i + thread_num] for i in range(0, len(code_list), thread_num)]
        threadList = []
        for code_list_spilt in all_code_list:
            t = threading.Thread(target=self.batch_fetch_data, args=[code_list_spilt, ])
            threadList.append(t)
        for t in threadList:
            t.start()
        for t in threadList:
            t.join()