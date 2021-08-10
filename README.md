# US stock service crawling project
---------------------------

# Project summary
## service architecture
![initial](https://user-images.githubusercontent.com/80030759/124936355-6a8c2e80-e041-11eb-94fd-8f612cdda68c.png)

# 1. Crawling
------------------------
 * Crawling Data
   
    - stock news
      - investing domain URL
      - naver stock
    - Stock data
      - FDR library
   
# 2. Data base system
  - GCP(mysql)
    
    - ERD
 
![initial](https://user-images.githubusercontent.com/80030759/126607523-5f38be1e-c143-4d3b-8d5d-2c7cf4c23143.png)


  - other

# 3. Web API server
  - Flask

# 4. Service
  - DashBoard
    - BootStrap
    - chart.js
  - chatbot

------------
# 5. Manual
### Manual.ipynb 참고
 
------------
# 6. 실행화면
 <결과><br/>
 SP500에 포함된 505개의 종목을 중심으로 매일 데이터를 수집하여 각 종목에 맞는 차트와 뉴스를 제공하는 웹 어플리케이션을 제작하여 서비스를 제공하였습니다.
 
![initial](https://user-images.githubusercontent.com/80030759/128801139-0cc9aaf5-5b5f-4683-a162-3b65c4771382.png)
![initial](https://user-images.githubusercontent.com/80030759/128801215-afda9ee0-0dde-4fe6-9031-d4e952cb6b44.png)


# 7. 역할
김상구 - 크롤링 / Flask <br/>
조경수 - HTML / Flask <br/>
이지영 - 데이터베이스 / HTML / README <br/>

# 8. 우리가 배운점, 그리고...
카카오톡 챗봇을 반영해 웹에 손쉽게 접근하게 하고 싶었으나 카카오챗봇 권한 문제로 인해 적용을 하지 못한게 아쉬웠으며, DB관리에 대한 어려움을 느꼇습니다. 수집한 Data를 저장해 DB를 불러오는 Query 작성에 이르기까지 여러 부분에 있어서 쉽지 않았습니다. 이러한 부분을 계속 개선시켜 발전시킬 필요가 있을것 같습니다.
환경설정에 있어 어려움을 경험 하였습니다. windows, mac, linux까지 다양한 환경에서 작업이 이루어져 path 설정 등 다양한 문제를 경험하였으며 그러한 문제를 해결하는데 만은 시간을 사용하였습니다.
