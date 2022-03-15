# Scraping-stock-market-websites-investing.com-and-egx.com-using-selenium-and-bs4-

## What do we scrape using this code?

1. First, we scrape all the egyptian comapnies data from : https://egx.com.eg/en/ListedStocks.aspx
2. We search by company code in https://www.investing.com
3. for each company, we scrape four things:
 
      a. Company general data
      
      ![image](https://user-images.githubusercontent.com/47758339/158309128-ac478174-696c-4752-986b-f8e0dae3d3e6.png)

      b. Annual Financial Summary, we use firefox selenuim to switch from quarterly to annual
      
      ![image](https://user-images.githubusercontent.com/47758339/158309013-9a4d1ac3-e718-48bc-9451-639818f18877.png)

      c. financial Dividends
      
      ![image](https://user-images.githubusercontent.com/47758339/158308812-bef2de85-73d5-47e2-ab41-d00582f34912.png)


4. process the results, convert them into numeric, and save all the results into excel



## How to run this code:

### 1. Using Jupiter Notebook

   a. download and run the notebook
    
    Scraping stock market websites, investing.com and egx.com, using selenium and bs4 .ipynb
    
   b. Download and unzib geckodriver-v0.30.0-win64.zip at the same directory to be able to use selenuim with firefox
    
   c. run code
    


### 2. using command line


  1. download the .py files with unzipping geckodriver-v0.30.0-win64.zip in the same directory
  2. run scrape.py code


