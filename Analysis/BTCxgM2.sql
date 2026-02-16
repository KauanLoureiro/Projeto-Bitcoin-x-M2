-- Para analise
SELECT t1.*, t2.BTC_price_M
FROM M2_global AS t1


LEFT JOIN BTC_DOL AS t2
ON t1.Month = t2.Month