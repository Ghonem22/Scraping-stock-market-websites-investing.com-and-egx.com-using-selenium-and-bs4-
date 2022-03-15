from utilis import *

# initialize driver 
profile = webdriver.FirefoxProfile()

profile.set_preference("dom.webnotifications.enabled", False)
profile.set_preference("dom.push.enabled", False)

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options, firefox_profile=profile)


# driver = webdriver.Firefox()
driver.maximize_window()



# run code
resutls, not_exist, skipped_urls, home_page_attrs, summary_attrs, summary_years= run()


# save results

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M")
  

    
# ********************************************************* save data *********************************************************

df1= pd.DataFrame (resutls, columns = ['item','Company Name', 'ISIN CODE', 'SECTOR','Ticker' ,'Ex-Dividend Date', 'Dividend EGP','Type', 'Payment Date', 'Yield'])
df1.loc[df1["Dividend EGP"] == "", "Dividend EGP"] = 0
df1["Dividend EGP"] = df1["Dividend EGP"].astype(str).astype(float)
df1['Dividend EGP'] = df1['Dividend EGP'].map(lambda a: round(a,3))

df1['Yield'] = df1['Yield'].map(lambda a: a.replace('%', ''))
df1.loc[df1["Yield"] == "-", "Yield"] = 0
df1["Yield"] = df1["Yield"].astype(str).astype(float) / 100
df1['Yield'] = df1['Yield'].map(lambda a: round(a,3))


df1['Ex-Dividend Date'] = df1['Ex-Dividend Date'].map(lambda a: a.replace(a[:4], str(datetime.strptime(a[:3], "%b").month) +'/' ))
df1['Ex-Dividend Date'] = df1['Ex-Dividend Date'].map(lambda a: a.replace(', ', '/' ))
df1['Ex-Dividend Date']= pd.to_datetime(df1['Ex-Dividend Date'])


df1.loc[df1["Payment Date"] == "--", "Payment Date"] = 'Jan 01, 2200'
df1['Payment Date'] = df1['Payment Date'].map(lambda a: a.replace(a[:4], str(datetime.strptime(a[:3], "%b").month) +'/' ))
df1['Payment Date'] = df1['Payment Date'].map(lambda a: a.replace(', ', '/' ))
df1['Payment Date']= pd.to_datetime(df1['Payment Date'])

df1.to_excel (f'data_{dt_string}.xlsx', index = False, header=True)


if not_exist:
    df2= pd.DataFrame (not_exist, columns = ['Company Name', 'ISIN CODE', 'SECTOR'])
    df2.to_excel (f'not_exist_data_{dt_string}.xlsx', index = False, header=True)

    
if skipped_urls:
    df3= pd.DataFrame (skipped_urls)
    df3 = df3[[0, 1, 2, 3]]
    df3 = df3.rename(columns={0: 'Company Name', 1: 'ISIN CODE', 2:'SECTOR' , 3: 'url'})
    df3.to_excel (f'No_data_to_display_{dt_string}.xlsx', index = False, header=True)
    
    

# ********************************************************* save summary_years *********************************************************
df_summary_years= pd.DataFrame(summary_years)
df_summary_years.reset_index(inplace = True)
df_summary_years.to_excel (f'summary_years_data_{dt_string}.xlsx', index = False, header=True)



# ********************************************************* save home page attr *********************************************************

def conv_to_num_dtype(df, col, not_found = '-', dtype = float):
    df.loc[df[col] == not_found, col] = 0
    
    df[col] = df[col].map(lambda a: str(a).replace(',', ''))
    df[col] = df[col].astype(str).astype(dtype)
    
    if dtype != int:
        df[col] = df[col].map(lambda a: round(a,2))
    return  df   

def get_num_sym(num):
    s = num[-1]
    if s == 'M':
        num = float(num[:-1]) * 1e6
    elif s == 'B':
        num = float(num[:-1]) * 1e9
    return num

df_home_page_attrs = pd.DataFrame(home_page_attrs) 

# split ranges
df_home_page_attrs["Day's Range1"] = df_home_page_attrs["Day's Range"].map(lambda a: a.split("-")[0])
df_home_page_attrs["Day's Range2"] = df_home_page_attrs["Day's Range"].map(lambda a: a.split("-")[1])
del df_home_page_attrs["Day's Range"]

df_home_page_attrs['52 wk Range1'] = df_home_page_attrs["52 wk Range"].map(lambda a: a.split("-")[0])
df_home_page_attrs['52 wk Range2'] = df_home_page_attrs["52 wk Range"].map(lambda a: a.split("-")[1])
del df_home_page_attrs["52 wk Range"]

# conv B and M to num
df_home_page_attrs["Revenue"] = df_home_page_attrs["Revenue"].map(lambda a: get_num_sym(a))
df_home_page_attrs["Market Cap"] = df_home_page_attrs["Market Cap"].map(lambda a: get_num_sym(a))

# conv to date type
df_home_page_attrs.loc[df_home_page_attrs["Next Earnings Date"] == "-", "Next Earnings Date"] = 'Jan 01, 2200'
df_home_page_attrs['Next Earnings Date'] = df_home_page_attrs['Next Earnings Date'].map(lambda a: a.replace(a[:4], str(datetime.strptime(a[:3], "%b").month) +'/' ))
df_home_page_attrs['Next Earnings Date'] = df_home_page_attrs['Next Earnings Date'].map(lambda a: a.replace(', ', '/' ))
df_home_page_attrs['Next Earnings Date']= pd.to_datetime(df_home_page_attrs['Next Earnings Date'])

# remove %
df_home_page_attrs['1-Year Change'] = df_home_page_attrs['1-Year Change'].map(lambda a: a.replace('%', ''))
df_home_page_attrs.loc[df_home_page_attrs["1-Year Change"] == "-", "1-Year Change"] = 0
df_home_page_attrs["1-Year Change"] = df_home_page_attrs["1-Year Change"].astype(str).astype(float) / 100
df_home_page_attrs['1-Year Change'] = df_home_page_attrs['1-Year Change'].map(lambda a: round(a,3))


# Prev. Close to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'Prev. Close')

# Open to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'Open')

# EPS to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'EPS')

# Volume to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'Volume')

# Average Vol. (3m)	 to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'Average Vol. (3m)')

# Shares Outstanding to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'Shares Outstanding')

# P/E Ratio to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'P/E Ratio')

# Day's Range1 to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, "Day's Range1")

# Day's Range2 to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, "Day's Range2")

# 52 wk Range1 Ratio to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, '52 wk Range1')

# 52 wk Range2 to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, '52 wk Range2')

# Beta to float
df_home_page_attrs = conv_to_num_dtype(df_home_page_attrs, 'Beta')



# save result
df_home_page_attrs.to_excel (f'home_page_data_{dt_string}.xlsx', header=True)



# ********************************************************* save summary attrs *********************************************************

df_summary_attrs= pd.DataFrame(summary_attrs)
df_summary_attrs.to_excel (f'summary_attrs_data_{dt_string}.xlsx', header=True)

