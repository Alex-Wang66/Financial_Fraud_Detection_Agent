# 数据获取和指标提取说明 | Data Fetching & Indicators Extraction Guide

## 📊 三大部分数据架构

本项目的数据流程包括三个核心部分（集成自本地Notebook项目）：

```
┌─────────────────────────────────────────────────────────────────┐
│                    财务欺诈检测系统数据流                        │
└─────────────────────────────────────────────────────────────────┘

1️⃣  数据获取层 (Data Fetcher)
    ├─ OpenBB SDK (推荐)
    ├─ FMP API (备用)
    ├─ NEWSAPI (新闻数据)
    └─ SEC EDGAR (监管数据)
              ↓
2️⃣  数据格式化层 (Indicator Extractor)
    ├─ 财务指标标准化
    ├─ 新闻数据结构化
    └─ SEC信息提取
              ↓
3️⃣  分析层 (Analysis Pipeline)
    ├─ 风险评分计算
    ├─ 异常检测
    └─ 报告生成
```

---

## 🔍 第一部分：数据获取 (get_company_financials)

### 概述

使用 **OpenBB SDK** 和 **FMP API** 从真实数据源获取公司财务数据。

### 支持的数据类型

#### 1. **财务报表数据**

从FMP Financial Database获取：

- **收入报表 (Income Statement)**
  - 收入 (Revenue)
  - 成本 (Cost of Goods Sold)
  - 毛利 (Gross Profit)
  - 净利润 (Net Income)

- **资产负债表 (Balance Sheet)**
  - 总资产 (Total Assets)
  - 流动资产 (Current Assets)
  - 总负债 (Total Liabilities)
  - 股东权益 (Shareholders' Equity)

- **现金流量表 (Cash Flow Statement)**
  - 运营现金流 (Operating Cash Flow)
  - 投资现金流 (Investing Cash Flow)
  - 融资现金流 (Financing Cash Flow)

#### 2. **关键财务指标**

- ROA, ROE, 净利率等
- 债务比率、流动比率等
- 资产周转率、库存周转率等

### 使用示例

```python
from fraud_detection.core import DataFetcher, fetch_financial_report

# 方式1: 使用便捷函数
report = fetch_financial_report(
    ticker='AAPL',
    fmp_api_key='your_fmp_key',
    newsapi_key='your_newsapi_key'
)

# 方式2: 使用DataFetcher类
fetcher = DataFetcher(
    fmp_api_key='your_fmp_key',
    newsapi_key='your_newsapi_key'
)

# 获取财务数据
financials = fetcher.fetch_company_financials('AAPL')
print(f"Income Statement: {financials['data']['income_statement']}")
print(f"Balance Sheet: {financials['data']['balance_sheet']}")
print(f"Cash Flow: {financials['data']['cash_flow_statement']}")

# 获取新闻
news = fetcher.fetch_company_news('AAPL', days=30)
for article in news:
    print(f"{article['title']} - {article['sentiment']}")

# 获取SEC Filings
filings = fetcher.fetch_sec_filings('AAPL', filing_type='10-K')

# 编译完整报告
report = fetcher.compile_financial_report('AAPL')
```

### 配置API密钥

```bash
# 创建 .env 文件
cat > .env << EOF
FMP_API_KEY=your_fmp_key_here
NEWSAPI_KEY=your_newsapi_key_here
EOF
```

**获取API密钥**:
1. **FMP API**: https://financialmodelingprep.com/
2. **NewsAPI**: https://newsapi.org/
3. **OpenBB**: 使用 `obb.user.credentials.fmp_api_key = "your_key"`

---

## 📋 第二部分：指标提取和格式化 (extract_key_indicators)

### 概述

将获取的原始数据**格式化和结构化**为标准的财务指标。

### 支持的提取方式

#### 方式1：从财务报表直接提取

```python
from fraud_detection.core import extract_from_dict

# 从结构化财务数据中提取指标
financial_data = {
    'revenue': 383285000000,
    'net_income': 93736000000,
    'cash_and_equivalents': 39572000000,
    'total_assets': 348988000000,
    'total_liabilities': 147177000000,
    'shareholders_equity': 201811000000,
    'free_cash_flow': 119437000000,
    # ... 其他字段
}

indicators = extract_from_dict(financial_data)
print(f"Revenue: ${indicators.revenue:,.0f}")
print(f"Net Income: ${indicators.net_income:,.0f}")
print(f"Confidence: {indicators.confidence_score:.2%}")
```

#### 方式2：从文本财务报告提取（使用LLM）

```python
from fraud_detection.core import KeyIndicatorExtractor

extractor = KeyIndicatorExtractor()

# 从财务报告文本智能提取
report_text = """
Apple Inc. Q4 2024财务报告
收入：$89.5 billion
净利润：$22.6 billion
...
"""

indicators = extractor.extract_from_text(
    financial_report_text=report_text,
    company_name="Apple Inc."
)

print(f"Revenue: ${indicators.revenue:,.0f}")
print(f"Confidence: {indicators.confidence_score:.2%}")
```

#### 方式3：批量提取多个报告

```python
# 批量提取多个公司数据
reports = [
    ("Apple财务数据...", "Apple Inc."),
    ("Microsoft财务数据...", "Microsoft"),
    ("Google财务数据...", "Alphabet Inc."),
]

results = extractor.batch_extract(reports)
for indicators in results:
    print(f"{indicators.company_name}: Confidence {indicators.confidence_score:.2%}")
```

### 提取的标准格式

```python
@dataclass
class ExtractedIndicators:
    # 文本指标
    audit_opinion: str  # Unqualified/Qualified/Adverse/Disclaimer
    industry_category: str  # 行业分类
    negative_news_count: int  # 负面新闻数量
    tone_factor: str  # Positive/Neutral/Negative
    
    # 数值指标
    revenue: float  # 收入
    net_income: float  # 净利润
    cash_and_equivalents: float  # 现金及等价物
    total_assets: float  # 总资产
    total_liabilities: float  # 总负债
    shareholders_equity: float  # 股东权益
    free_cash_flow: float  # 自由现金流
    
    # 元数据
    extraction_source: str  # 提取来源
    confidence_score: float  # 置信度 (0.0-1.0)
    extraction_timestamp: str  # 提取时间戳
```

---

## 📊 第三部分：完整的数据处理流程

### 从数据获取到分析的完整流程

```python
from fraud_detection.core import (
    DataFetcher,
    KeyIndicatorExtractor,
    AnalysisPipeline
)

# Step 1: 获取真实数据
fetcher = DataFetcher(fmp_api_key='...', newsapi_key='...')
financial_report = fetcher.compile_financial_report('AAPL')

# Step 2: 提取和格式化指标
extractor = KeyIndicatorExtractor()
indicators = extractor.extract_from_structured_data(
    financial_report['components']['financial_data']['data']
)

# Step 3: 运行欺诈分析
pipeline = AnalysisPipeline()
analysis_result = pipeline.run_analysis(
    ticker='AAPL',
    company_name='Apple Inc.',
    current_metrics={
        'revenue': indicators.revenue,
        'net_income': indicators.net_income,
        'cash_and_equivalents': indicators.cash_and_equivalents,
        # ... 其他指标
    }
)

# 获取结果
print(f"Risk Score: {analysis_result['anomalies']['risk_score']}")
print(f"Risk Level: {analysis_result['anomalies']['risk_level']}")
print(f"Fraud Score: {analysis_result['fraud_metrics']['score']}")
```

### REST API - 完整流程端点

```bash
# 1. 获取财务数据
curl -X POST http://localhost:5000/api/data/fetch \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# 2. 提取指标
curl -X POST http://localhost:5000/api/extract/indicators \
  -H "Content-Type: application/json" \
  -d '{"financial_data": {...}}'

# 3. 执行完整分析
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "current_metrics": {...}}'
```

---

## 🔄 数据流概览表

| 步骤 | 数据来源 | 操作 | 输出 |
|------|---------|------|------|
| **第1步** | OpenBB/FMP/NEWSAPI | 数据获取 | 原始财务数据、新闻、SEC信息 |
| **第2步** | 第1步的输出 | 指标提取 | 标准化的指标（ExtractedIndicators） |
| **第3步** | 第2步的输出 | 指标计算 | 财务比率（ROA、ROE等） |
| **第4步** | 第3步的输出 | 异常检测 | 风险因子和风险评分 |
| **第5步** | 第4步的输出 | 报告生成 | HTML仪表板和分析报告 |

---

## 📐 数据标准和映射

### 字段映射表

提取器支持多种字段名称自动映射：

```python
numeric_mappings = {
    'revenue': ['revenue', 'totalRevenue', 'sales', 'income'],
    'net_income': ['netIncome', 'net_profit', 'net_earnings'],
    'cash_and_equivalents': ['cash', 'cashEquivalents', 'cash_and_equivalents'],
    'total_assets': ['totalAssets', 'assets'],
    'total_liabilities': ['totalLiabilities', 'liabilities'],
    'shareholders_equity': ['shareholdersEquity', 'equity', 'stockholdersEquity'],
    'free_cash_flow': ['freeCashFlow', 'fcf', 'free_cash_flow'],
}
```

### 信心评分的计算

```
信心评分 = (提取字段数 / 总字段数) × 100%

示例:
- 提取了7个数值字段 + 4个文本字段 = 信心评分 91%
- 缺失审计意见但其他数据完整 = 信心评分 85%
```

---

## ⚙️ 配置和优化

### 性能优化

```python
# 缓存获取结果
from functools import lru_cache

@lru_cache(maxsize=100)
def get_company_data(ticker):
    fetcher = DataFetcher()
    return fetcher.fetch_company_financials(ticker)
```

### 错误处理

```python
import logging

logging.basicConfig(level=logging.INFO)

try:
    report = fetch_financial_report('AAPL')
except Exception as e:
    print(f"Error fetching data: {e}")
    # 使用备用数据或缓存
```

### 扩展自定义提取器

```python
from fraud_detection.core import KeyIndicatorExtractor

class CustomExtractor(KeyIndicatorExtractor):
    def extract_from_text(self, text, company_name=None):
        # 自定义提取逻辑
        result = super().extract_from_text(text, company_name)
        # 添加自定义处理
        return result
```

---

## 📚 版本历史

**v2.0.2** (当前)
- ✨ 添加真实数据获取模块 (DataFetcher)
- 🔗 集成OpenBB SDK和FMP API
- 📰 添加NEWSAPI支持
- 📋 支持SEC EDGAR filing获取

**v2.0.1**
- ✨ 添加关键指标智能提取模块
- 🤖 LLM多后端支持

**v2.0.0**
- 🎯 完整的欺诈检测系统

---

## 🔗 相关资源

- [OpenBB Documentation](https://docs.openbb.co/)
- [FMP API Documentation](https://financialmodelingprep.com/developer/docs/)
- [NewsAPI Documentation](https://newsapi.org/)
- [SEC EDGAR API](https://www.sec.gov/edgar)

---

**Note**: 所有API密钥应该安全存储，不要直接提交到GitHub。使用 `.env` 文件和环境变量。
