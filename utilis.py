
# import reqired libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
from numpy.random import uniform
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import numpy as np
#use BeautifulSoup for easier html extraction
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import random 
import pandas as pd

# some diffrent user_agent
user_agents = [ 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    ] 


user_agent = random.choice(user_agents) 
hdr = {'User-Agent': user_agent} 


delay=3
def wait_until_elem(type,selec,delay):

    try:
        wait = WebDriverWait(driver, delay)
        if type=='ID':
            wait.until(EC.presence_of_element_located((By.ID, selec))) 
        elif type=='CLASS':
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, selec))) 
        #wait until searchform loadded to the page
        #we search here using the ID
        print("Page is ready")
    except TimeoutException:
        print("Loading took too much time")

def clode_pop():
    
    try:
        time.sleep(.2)
        driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
        time.sleep(.2)
        driver.find_element_by_xpath('//*[@id="rsdiv"]/div[3]/div[1]').click()
        driver.find_element_by_xpath('//*[@id="rsdiv"]/div[3]/div[1]').click()
        print('closed pop')
    except:
        print('no pop')





# important function


def get_soup(page_url):
    driver.get(page_url)
    main_page = driver.current_window_handle

    # wait till page load
    try:
        time.sleep(2)
        clode_pop()
    except:
        wait_until_elem('CLASS',"companySummaryIncomeStatement",6)
        clode_pop()
    # move to annual
    try:
        driver.switch_to.window(main_page)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='leftColumn']/div[9]/a[1]"))).click()
        print("is completed direc")
    except:
        # if there is pop page, close it then try to move to annual again
        try:
            driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
            time.sleep(.2)
            driver.find_element_by_xpath('//*[@id="rsdiv"]/div[3]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="rsdiv"]/div[3]/div[1]').click()
        except:
            pass

        time.sleep(.2)
        driver.find_element_by_xpath('//*[@id="rsdiv"]/div[3]/div[1]').click()
        driver.find_element_by_xpath('//*[@id="rsdiv"]/div[3]/div[1]').click()
        time.sleep(.2)
        driver.switch_to.window(main_page)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='leftColumn']/div[9]/a[1]"))).click()
        print("is completed through exception")
    
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')


def get_years(table):
    years_data = table.find_all('th')
    years =  [int((year.text).split(', ')[-1]) for year in years_data[1:]]
    n = 4 - len(years) 
    if n > 0:
        add = [-1000] * n
        years.extend(add)
    elif n < 0:
        del years[n:]
    return years

def table_content(tables, i):
    # all the three tables wih the same tage, so we will use them with i
    table = tables[i]
    data = {}
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 0 or cols[2].text.strip() == '12 Months':
            continue
        cols_data = [ele.text.strip() for ele in cols]
        cols = cols_data[1:]
        cols = [i if i != '' else -1000 for i in cols]

        if len(cols) == 0:
            cols = [-10000,-10000, -10000, -10000]
        
        n = 4 - len(cols) 
        if n > 0:
            add = [-1000] * n
            cols.extend(add)
        elif n < 0:
            del cols[n:]
        key = cols_data[0]
        data[key] = [float(ele) for ele in cols if ele] # Get rid of empty values
    return data

# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

def get_summary(soup):
    summary = {}
    tables = soup.find_all('table', attrs={"class": "genTbl openTbl companyFinancialSummaryTbl"})
    years = get_years(tables[0])
        
    summary.update({'years': years})
    for i in range(len(tables)):
        summary.update(table_content(tables, i))
    
#     summary = np.array(data).T.tolist()

    return summary


def get_summary_attributes(soup):

    results = soup.find_all('div', attrs={"class": "infoLine"})
    output = {}
    for result in results:
        result = result.text.strip()
        key = result.split("  ")[0]
        string_encode = key.encode("ascii", "ignore")
        key = string_encode.decode()
        value = result.split("  ")[1]
    #     value = result[1].replace("\n", "").strip()
        if value == '-':
            value = -1
        else:
            value = round(float(value.replace("%", "")) / 100,4)

        if key not in output.keys():
            output[key] = value
        else:
            output[key].append(value)
    return output

def get_main_page_attr(url):
    output = {}
    req = Request(url, headers= hdr)
    text = urlopen(req).read()
    soup = BeautifulSoup(text,"lxml")
    results = soup.find_all('div', attrs={"class": "flex justify-between border-b py-2 desktop:py-0.5"})
    for result in results:
        key = result.find('dt').text
        value = result.find('dd').text
        if key not in output.keys():
            output[key] = value
        else:
            output[key] = [output[key]]
            output[key].append(value)
    return output

# validate if the url start with the domain, if notL add the domain
def validate_url_domain(url, domain):
    if not url.startswith("http"):
        url = domain + url
    return url

def get_egx_data(url = "https://egx.com.eg/en/ListedStocks.aspx"):
#     user_agent = random.choice(user_agents) 
#     hdr = {'User-Agent': user_agent} 
    print(hdr)
    req = Request(url, headers= hdr)
    text = urlopen(req).read()
    soup = BeautifulSoup(text,"lxml")
    table = soup.find('table', attrs={"id": "ctl00_C_L_GridView2"})
    rows = table.find_all('tr')
    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 0:
            continue
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data


def get_investing_url(egx_code):
#     user_agent = random.choice(user_agents) 
#     hdr = {'User-Agent': user_agent} 
    search_url = f"https://www.investing.com/search/?q={egx_code}"
    print(search_url)
    req = Request(search_url, headers= hdr)
    text = urlopen(req).read()
    soup = BeautifulSoup(text,"lxml")
    url = soup.find('a', attrs={"class": "js-inner-all-results-quote-item row"})
    validated_url = validate_url_domain(url['href'], "https://www.investing.com")
    
    dividend_url = validated_url.split("?")[0] + '-dividends'
    summary_url = validated_url.split("?")[0] + '-financial-summary'
    return validated_url, dividend_url, summary_url


def get_dividends(page_url):
    data = []
    req = Request(page_url, headers= hdr)
    text = urlopen(req).read()
    soup = BeautifulSoup(text,"lxml")
    table = soup.find('table', attrs={"class": "genTbl closedTbl dividendTbl"})
    Ticker_soup = soup.find('div', attrs={"class": "instrumentHeader"})

    if Ticker_soup and table:
        Ticker = Ticker_soup.h2.text.split()[0]
        rows = table.find_all('tr')
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 0:
                continue
            item_type = row.find_all('td')[2].span.get("title")
            cols = [ele.text.strip() for ele in cols]
            del cols[2]
            cols.insert(0, Ticker)
            cols.insert(3, item_type)
            data.append(cols) 

    # if no Dividends
    if Ticker_soup and not table:
        cols = ['','','','','','']
        Ticker = Ticker_soup.h2.text.split()[0]
        cols[0] = Ticker
        data.append(cols) 

    return data



# collect all together

def run():
    # dividend_data
    resutls = []
    not_exist = []
    skipped_urls = []
    
    # home_page_attrs
    home_page_attrs = {
            "Company Name":[],
            "ISIN CODE": [],
            "SECTOR": [],
            "Ticker": [],
            "Prev. Close": [],
            "Day's Range": [],
            'Revenue': [],
            'Open': [],
            '52 wk Range': [],
            'EPS': [],
            'Volume': [],
            'Market Cap': [],
            'Dividend (Yield)': [],
            'Average Vol. (3m)': [],
            'P/E Ratio': [],
            'Beta': [],
            '1-Year Change': [],
            'Shares Outstanding': [],
            'Next Earnings Date': []
    }


    # summary attrs
    
    summary_attrs = {
            "Company Name":[],
            "ISIN CODE": [],
            "SECTOR": [],
            "Ticker": [],
            'Gross marginTTM': [],
            'Operating marginTTM':  [],
            'Net Profit marginTTM':  [],
            'Return on InvestmentTTM': [],
            'Quick RatioMRQ':  [],
            'Current RatioMRQ':  [],
            'LT Debt to EquityMRQ': [],
            'Total Debt to EquityMRQ': [],
            'Cash Flow/ShareTTM':  [],
            'Revenue/ShareTTM':  [],
            'Operating Cash Flow': []
        }


    # summary_years
    summary = {}
    
    try:
        egx_data = get_egx_data()
        print("scrapping all codes sucsessfully")
    except:
        time.sleep(60)
        egx_data = get_egx_data()
        print("scrapping all codes sucsessfully")

    for i, item in enumerate(egx_data):

        user_agent = random.choice(user_agents) 
        hdr = {'User-Agent': user_agent} 
        egx_code = item[1]

        try:
            validated_url, dividend_url, summary_url = get_investing_url(egx_code)
            time.sleep(uniform(.5, 1))
        except:
            
            not_exist.append([item[0],item[1], item[2]])
            print(f"company with code {egx_code} not exist @ investing.com ")
            continue

        # get dividend
        try:
            print(i)
            dividends = get_dividends(dividend_url)
            ticker_for_attr = dividends[0][0]
            if dividends[0][1] == '':
                skipped_urls.append([item[0],item[1], item[2], dividend_url])
                print(f"company with url: {dividend_url} has no data @ investing.com")
                continue

            for dividend in dividends:
                dividend.insert(0,i +1)
                dividend.insert(1,item[0])
                dividend.insert(2,item[1])
                dividend.insert(3,item[2])
                resutls.append(dividend)
                time.sleep(uniform(.5, 1))

        except:
            skipped_urls.append([item[0],item[1], item[2], dividend_url])
            time.sleep(uniform(2, 4))
            # print(f"error with:   {dividend_url}")
        

        # get summary years
        try:
            
            soup = get_soup(summary_url)
            indices = [i + 1] * 4
            comp_name = [item[0]] * 4
            code =  [item[1]] * 4
            sector = [item[2]] * 4
            ticker = [ticker_for_attr] * 4


            year_attr = {
                "item":indices,
                "Company Name": comp_name,
                "ISIN CODE": code,
                "SECTOR": sector,
                "Ticker": ticker
                    }


            years_summary = get_summary(soup)

            year_attr.update(years_summary)

            if i == 0:
                summary_years = pd.DataFrame(year_attr)   
            else:
                summary = pd.DataFrame(year_attr)   
                summary_years = pd.concat([summary_years, summary], axis=0)
            
#         summary = np.array(years_summary).T.tolist()
#         summary_years.extend(summary)
        
    
        # get summary attr
            attr = {

                "Company Name": item[0],
                "ISIN CODE": item[1],
                "SECTOR": item[2],
                "Ticker": ticker_for_attr
                    }
            summary_attr = get_summary_attributes(soup)

            for key in summary_attrs.keys():
                if key in ["Company Name", "ISIN CODE", "SECTOR", "Ticker"]:
                    summary_attrs[key].append(attr[key])
                else:
                    summary_attrs[key].append(summary_attr[key])
        except:
            print(f"error while scraping summary {summary_url}")

            
            
        try:

            # get home_page

            home_page_attr = get_main_page_attr(validated_url)
            for key in home_page_attrs.keys():
                if key in ["Company Name", "ISIN CODE", "SECTOR", "Ticker"]:
                    home_page_attrs[key] = attr[key]
                else:
                    home_page_attrs[key].append(home_page_attr[key])
        except:
            print(f"err with home page  {validated_url}")
            
#         if i > 5:
    return resutls, not_exist, skipped_urls, home_page_attrs, summary_attrs, summary_years
