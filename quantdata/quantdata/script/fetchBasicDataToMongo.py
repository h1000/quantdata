from quantdata import logger
from quantdata.stock import quotes
from quantdata.db.mongo import Mongo



def run():
    LOGGER_NAME = "UPDATE_DATA"
    mylog = logger.getLogger(LOGGER_NAME)
    mongodb = Mongo()
    stokList = quotes.get_stock_hq_list()
    for code in stokList["code"]:
        mylog.info("update mainreport data of %s"%(code))
        mongodb.updateMainReport(code)
        
if __name__ == '__main__':
    
    run()