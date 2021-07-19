/* 테슬라 6월 종가 기록
	SELECT Date, Close
	FROM US_Stock.daily
	WHERE DATE(Date) BETWEEN "2021-06-01" AND "2021-06-28" AND Symbol = "TSLA";
	*/
/* 테슬라와 동일한 산업의 시총
SELECT Industry, SUM(market capitalzation)
    FROM US_Stock.company, US_Stock.daily
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol and DATE(Date)="2021-06-28" and Industry = 'Automobile Manufacturers'
    GROUP BY Industry
    ORDER BY SUM(market capitalzation) desc;
    */
/* S&P500 종가 기록
SELECT Date, Close
	FROM US_Stock.daily
	WHERE DATE(Date) BETWEEN "2006-01-04" AND "2021-02-10" AND Symbol = "US500;
	*/
/* Sector별 평균 거래량
SELECT Sector, AVG(volume)
	FROM US_Stock.company, US_Stock.daily
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol and DATE(Date)="2021-06-28"
    GROUP BY Sector
    ORDER BY AVG(volume) desc;
*/
/* 하루전, 한달전, 3달전, 1년 전 종가 검색 
SELECT Symbol, Close, Date
    FROM US_Stock.daily
    WHERE Date = DATE_ADD("2021-06-28", INTERVAL -1 MONTH) and ("2021-06-28")
    ORDER BY Close DESC;

SELECT Name, Close, Date
    FROM US_Stock.company, US_Stock.daily
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol and Date = DATE_ADD("2021-06-28", INTERVAL -3 DAY) and ("2021-06-28")
    ORDER BY Close DESC;
    

SELECT Name, Close, Date
    FROM US_Stock.company, US_Stock.daily
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol and Date = DATE_ADD("2021-06-28", INTERVAL -1 MONTH) and ("2021-06-28")
    ORDER BY Close DESC;
    

SELECT Name, Close, Date
    FROM US_Stock.company, US_Stock.daily
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol and Date = DATE_ADD("2021-06-28", INTERVAL -3 MONTH) and ("2021-06-28")
    ORDER BY Close DESC;
    

SELECT Name, Close, Date
    FROM US_Stock.company, US_Stock.daily
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol and Date = DATE_ADD("2021-06-28", INTERVAL -1 YEAR) and ("2021-06-28")
    ORDER BY Close DESC;
*/

