-- =====================================================
-- Query 1
-- Total companies
-- =====================================================

SELECT COUNT(*) AS total_companies
FROM companies;


-- =====================================================
-- Query 2
-- Top 10 companies by ROE
-- =====================================================

SELECT
company_name,
roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;


-- =====================================================
-- Query 3
-- Companies with highest sales
-- =====================================================

SELECT
company_id,
year,
sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;


-- =====================================================
-- Query 4
-- Net profit by company
-- =====================================================

SELECT
company_id,
SUM(net_profit) AS total_profit
FROM profitandloss
GROUP BY company_id
ORDER BY total_profit DESC;


-- =====================================================
-- Query 5
-- Highest market cap
-- =====================================================

SELECT
company_id,
year,
market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;


-- =====================================================
-- Query 6
-- Largest debt
-- =====================================================

SELECT
company_id,
year,
borrowings
FROM balancesheet
ORDER BY borrowings DESC
LIMIT 10;


-- =====================================================
-- Query 7
-- Stock price history count
-- =====================================================

SELECT
company_id,
COUNT(*) AS records
FROM stock_prices
GROUP BY company_id
ORDER BY records DESC;


-- =====================================================
-- Query 8
-- Companies by sector
-- =====================================================

SELECT
broad_sector,
COUNT(*)
FROM sectors
GROUP BY broad_sector
ORDER BY COUNT(*) DESC;


-- =====================================================
-- Query 9
-- Peer groups
-- =====================================================

SELECT
peer_group_name,
COUNT(*)
FROM peer_groups
GROUP BY peer_group_name;


-- =====================================================
-- Query 10
-- Companies having analysis data
-- =====================================================

SELECT
company_id,
COUNT(*)
FROM analysis
GROUP BY company_id;