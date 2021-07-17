# Crawling_project
US stock service crawling project
---------------------------
* Project schedule ~ 7/9 BETA version 
  * S&P500 main page
  * TSLA main page
 
* ending Project : 7/23
  * using a crontap Auto Crailng data
  * All of S&P500 Stocks display
  * using a kakao chatbot
---------------------------
# Project Steps
# service architecture
![initial](https://user-images.githubusercontent.com/80030759/124936355-6a8c2e80-e041-11eb-94fd-8f612cdda68c.png)




# 1. Crawling
------------------------
* Using library

  - import requests
  - import pandas as pd
  - from bs4 import BeautifulSoup
------------------------
 * Crawling Data
   
    - stock news
      - investing domain URL
      - naver stock
    - other
----------------------  
 * Stock Data use a FinanceDataReader Python library
 
    - How to use
      - import FinanceDataReader as fdr
    - Target data
      - daily S&P500 data
# 2. Data base system
  - mysql
    
    - ERD
 
![initial](https://user-images.githubusercontent.com/80030759/122144633-d3431980-ce8e-11eb-957c-71e41d04d96f.png)

  - other

# 3. Data analysis
  - Flask
    - Chart.js (EDA)
  - MySQL

# 4. Service
  - chatbot
  - DashBoard
    - chart.js
    - BootStrap
 
![initial](https://user-images.githubusercontent.com/80030759/125158027-359aeb80-e1a9-11eb-9b80-411d9fe97e6e.png)
![initial](https://user-images.githubusercontent.com/80030759/125157072-c79ff580-e1a3-11eb-833c-619ada65766d.png)

