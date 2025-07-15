CREATE VIEW sales_reporting_view AS
SELECT
    SELECT 
  branch,
  SUM(total) AS total_sales
FROM  fact_sales f
GROUP BY branch
ORDER BY total_sales DESC
;