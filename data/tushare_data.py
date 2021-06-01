import pandas as pd
import os
import tushare as ts


ts_code = '000037.SZ'
start_date = '20000101'
end_date = '20210308'
df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
df.sort_values(by='trade_date', axis=0, inplace=True)
pd.to_datetime(df.trade_date, format='%Y/%m/%d')


# In[3]:


# 只下载一只股票数据，且只用CSV保存，未来可以有自己的数据库
def get_data(ts_code, start_date, end_date):
    ts.set_token('d377964ecaa07f68b033dac61fc0ee7cfcc8786099b5b799e1b222cc')
    pro = ts.pro_api()
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
    df.sort_values(by='trade_date', axis=0, inplace=True)
    # df = ts.get_k_data(code, autype='qfq', ktype="30",start=start, end=end)
    df.index = pd.to_datetime(df.trade_date, format='%Y/%m/%d')
    df.rename(columns={"vol": "volume"}, inplace=True)
    df['openinterest'] = 0.0  # Backtrader需要用到
    df = df[['open', 'high', 'low', 'close', 'volume', 'openinterest']]  # Backtrader规定的数据和列名
    df = df.dropna(axis=0, how='any')  # 删除表中含有任何NaN的行

    path = os.path.join(os.path.join(os.getcwd(), "data/RawData"), ts_code + ".csv")
    df.to_csv(path)

    print(df)
    #print("—" * 50)
    #print(df.info())
    #print("—" * 50)
    #print(df.describe())
    return df


# In[4]:


def get_from_csv(ts_code):
    data_file = os.path.join(os.path.join(os.getcwd(), "data/RawData"), ts_code + ".csv")  # 本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
    # print(数据地址)
    df = pd.read_csv(data_file, index_col="trade_date", parse_dates=True)
    # df =pd.read_csv(data_file,parse_dates = True)
    # df.trade_date=pd.to_datetime(df.trade_date,format='%Y/%m/%d')
    # print(data)
    print(df)
    print("—" * 50)
    print(df.info())
    print("—" * 50)
    print(df.describe())
    return df


# In[5]:


#ts_code = '000037.SZ'
#start_date = '20000101'
#end_date = '20210308'

#rawdata = get_data(ts_code, start_date, end_date)
