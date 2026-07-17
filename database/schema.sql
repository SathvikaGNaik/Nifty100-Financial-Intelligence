PRAGMA foreign_keys = ON;

--------------------------------------------------
-- Companies
--------------------------------------------------

CREATE TABLE IF NOT EXISTS companies (

    id TEXT PRIMARY KEY,

    company_logo TEXT,

    company_name TEXT NOT NULL,

    chart_link TEXT,

    about_company TEXT,

    website TEXT,

    nse_profile TEXT,

    bse_profile TEXT,

    face_value REAL,

    book_value REAL,

    roce_percentage REAL,

    roe_percentage REAL
);

--------------------------------------------------
-- Profit and Loss
--------------------------------------------------

CREATE TABLE IF NOT EXISTS profitandloss (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    year TEXT NOT NULL,

    sales REAL,

    expenses REAL,

    operating_profit REAL,

    opm_percentage REAL,

    other_income REAL,

    interest REAL,

    depreciation REAL,

    profit_before_tax REAL,

    tax_percentage REAL,

    net_profit REAL,

    eps REAL,

    dividend_payout REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

--------------------------------------------------
-- Balance Sheet
--------------------------------------------------

CREATE TABLE IF NOT EXISTS balancesheet (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    year TEXT,

    equity_capital REAL,

    reserves REAL,

    borrowings REAL,

    other_liabilities REAL,

    total_liabilities REAL,

    fixed_assets REAL,

    cwip REAL,

    investments REAL,

    other_asset REAL,

    total_assets REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

--------------------------------------------------
-- Cash Flow
--------------------------------------------------

CREATE TABLE IF NOT EXISTS cashflow (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year TEXT,

    operating_activity REAL,

    investing_activity REAL,

    financing_activity REAL,

    net_cash_flow REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

--------------------------------------------------
-- Analysis
--------------------------------------------------

CREATE TABLE IF NOT EXISTS analysis (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    compounded_sales_growth REAL,

    compounded_profit_growth REAL,

    stock_price_cagr REAL,

    roe REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

--------------------------------------------------
-- Documents
--------------------------------------------------

CREATE TABLE IF NOT EXISTS documents (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year TEXT,

    annual_report TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

--------------------------------------------------
-- Indexes
--------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_profit_company
ON profitandloss(company_id);

CREATE INDEX IF NOT EXISTS idx_balance_company
ON balancesheet(company_id);

CREATE INDEX IF NOT EXISTS idx_cash_company
ON cashflow(company_id);

CREATE INDEX IF NOT EXISTS idx_analysis_company
ON analysis(company_id);

CREATE INDEX IF NOT EXISTS idx_documents_company
ON documents(company_id);