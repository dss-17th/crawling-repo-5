# US stock service crawling project
---------------------------

# Project summary
## 1. service architecture
![initial](https://user-images.githubusercontent.com/80030759/124936355-6a8c2e80-e041-11eb-94fd-8f612cdda68c.png)

## 2. Crawling
------------------------
 * Crawling Data
   
    - stock news
      - investing domain URL
      - naver stock
    - Stock data
      - FDR library
   
## 3. Data base system
  - GCP(mysql)
    
    - ERD
 
![initial](https://user-images.githubusercontent.com/80030759/126607523-5f38be1e-c143-4d3b-8d5d-2c7cf4c23143.png)


  - other

## 4. Web API server
  - Flask

## 5. Service
  - DashBoard
    - BootStrap
    - chart.js
  - chatbot

------------
## 6. Manual
### Manual.ipynb 참고
 
------------
## 7. 실행화면
 <결과><br/>
 SP500에 포함된 505개의 종목을 중심으로 매일 데이터를 수집하여 각 종목에 맞는 차트와 뉴스를 제공하는 웹 어플리케이션을 제작하여 서비스를 제공하였습니다.
 
![initial](https://user-images.githubusercontent.com/80030759/128801139-0cc9aaf5-5b5f-4683-a162-3b65c4771382.png)
![initial](https://user-images.githubusercontent.com/80030759/128801215-afda9ee0-0dde-4fe6-9031-d4e952cb6b44.png)


## 8. 역할
김상구 - 크롤링 / Flask <br/>
조경수 - HTML / Flask <br/>
이지영 - 데이터베이스 / HTML / README <br/>

## 9. 우리가 배운점, 그리고...
우선 환경설정에 있어 어려움을 경험 하였습니다. windows, mac, linux까지 다양한 환경에서 작업이 이루어져 경로를 설정하는 등 다양한 부분에서 문제를 경험하였으며, 이것을 해결하는 데에 시간을 할애하였습니다.
또한 카카오톡 챗봇을 활용하여 웹에 손쉽게 접근하게 하고 싶었으나, 카카오 챗봇의 경우 권한 문제로 인해 활용을 할 수 없어 챗봇 구현을 하지 못한 부분이 아쉬웠으며,
DB관리에 대한 어려움 역시 있었습니다. 수집한 Data를 저장해 DB를 불러오는 Query 작성에 이르기까지 여러 부분에 있어서 쉽지 않았습니다. 이러한 부분을 계속 개선하여 발전시킬 필요가 있을 것 같습니다.
마지막으로 검색창을 활용하여 주식종목을 검색하는 것은 구현하는 데 어려움이 없었으나, 종목에 대한 다양한 검색어에 대처하는 부분에서 역시 어려움이 있었으나 이러한 부분은 지속적으로 개선해 나갈 예정입니다.
