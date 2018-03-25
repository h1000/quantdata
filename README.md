# quantdata
量化选股监控系统

* 股票数据采集
* 策略分析数据
* 策略监控股票功能

**开发环境** : `Centos 7.3` / `Python 3.6`/`Mysql`

#### 股票数据采集

* 从网上采集数据，包括基本面财务数据，K线数据存入Mysql

#### 股票数据分析

* 对采集好的数据，写策略分析数据，比如代码中有例子，分析筛选出产生业绩拐点的股票，然后输出报表

####  策略监控股票

* 对股票数据进行实时监控，例如监控早盘突然直线线拉升的股票，通过监控提醒，不用盯盘就可以反手做T了

####  例子：寻找业绩拐点股票
* 从同花顺抓取基本面数据  
`cd quantdata/analye`
`python ../data/main_report_json.py`
* 运行选股策略
`python guandian_json_v2.py`  
 生成一个execl文件  
 ![image](https://github.com/hezhenke/quantdata/blob/master/quantdata/pic/pic1.png)
