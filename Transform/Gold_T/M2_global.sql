-- SELECT 
--     t1.Month,
--     M2_cn_M_DOL+M2_eu_M_DOL+M2_jp_M_DOL+M2_us_M AS M2_global
-- FROM M2_cn_DOL AS t1

-- LEFT JOIN M2_eu_DOL AS t2
-- ON t1.Month=t2.Month

-- LEFT JOIN M2_jp_DOL AS t3
-- ON t1.Month=t3.Month

-- LEFT JOIN M2_us_DOL AS t4
-- ON t1.Month=t4.Month

SELECT t1.*, t2.M2_cn_M_DOL FROM M2_cn_CNY AS t1 LEFT JOIN M2_cn_DOL AS t2 ON t1.Month=t2.Month