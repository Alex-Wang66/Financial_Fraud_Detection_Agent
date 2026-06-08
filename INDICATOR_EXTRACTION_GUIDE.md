# 关键指标智能提取模块 | Key Indicators Extraction Module

## 📋 功能概述

`KeyIndicatorExtractor` 是一个智能指标提取模块，可以从财务报告**文本**中自动提取关键财务指标。

本模块从本地项目的 `extract_key_indicators.ipynb` 完整集成而来，支持多种LLM后端（讯飞Spark、OpenAI GPT等）进行智能提取。

---

## 🎯 核心功能

### 1. 文本智能提取（Text-based Extraction）

从自然语言财务报告中智能识别和提取数值及文本信息。

```python
from fraud_detection.core import KeyIndicatorExtractor, ExtractorBackend

# 初始化提取器
extractor = KeyIndicatorExtractor(backend=ExtractorBackend.MOCK)

# 提取指标
indicators = extractor.extract_from_text(
    financial_report_text="Apple Inc. Q4 2024财务报告...",
    company_name="Apple Inc."
)

# 访问结果
print(f"收入: {indicators.revenue}")
print(f"净利润: {indicators.net_income}")
print(f"审计意见: {indicators.audit_opinion}")
print(f"行业分类: {indicators.industry_category}")
print(f"提取置信度: {indicators.confidence_score:.2%}")
```

### 2. 结构化数据提取（Structured Data Extraction）

从已结构化的财务数据字典中提取指标。

```python
# 从结构化数据提取
financial_data = {
    'revenue': 383285000000,
    'net_income': 93736000000,
    'cash_and_equivalents': 39572000000,
    'audit_opinion': 'Unqualified',
    'industry_category': 'Technology',
    'tone_factor': 'Positive'
}

indicators = extractor.extract_from_structured_data(financial_data)
```

### 3. 批量提取（Batch Extraction）

高效处理多个财务报告的批量提取。

```python
# 批量提取多个公司
reports = [
    ("Apple财务报告文本...", "Apple Inc."),
    ("Microsoft财务报告文本...", "Microsoft"),
    ("Google财务报告文本...", "Alphabet Inc.")
]

results = extractor.batch_extract(reports)

for result in results:
    print(f"{result.company_name if hasattr(result, 'company_name') else 'Unknown'}: "
          f"置信度 {result.confidence_score:.2%}")
```

---

## 📊 提取的指标详解

### 文本指标（Textual Indicators）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `audit_opinion` | str | 审计意见 | Unqualified, Qualified, Adverse, Disclaimer |
| `industry_category` | str | 行业分类 | Technology, Finance, Healthcare, Manufacturing |
| `negative_news_count` | int | 负面新闻数量 | 2, 5, 0 |
| `negative_news_items` | List[str] | 具体负面新闻列表 | ['诉讼风险', '监管调查'] |
| `tone_factor` | str | 语调因子 | Positive, Neutral, Negative |

### 数值指标（Numerical Indicators）

| 字段 | 类型 | 说明 | 单位 |
|------|------|------|------|
| `revenue` | float | 收入/营收 | 货币 |
| `net_income` | float | 净利润/净收益 | 货币 |
| `cash_and_equivalents` | float | 现金及等价物 | 货币 |
| `total_assets` | float | 总资产 | 货币 |
| `total_liabilities` | float | 总负债 | 货币 |
| `shareholders_equity` | float | 股东权益 | 货币 |
| `free_cash_flow` | float | 自由现金流 | 货币 |

### 元数据字段（Metadata）

| 字段 | 类型 | 说明 |
|------|------|------|
| `extraction_source` | str | 提取来源 (mock/spark/openai) |
| `confidence_score` | float | 置信度分数 (0.0-1.0) |
| `extraction_timestamp` | str | 提取时间戳 |
| `raw_text_snippet` | str | 原始文本片段 |

---

## 🔧 支持的LLM后端

### 1. Mock 后端（模拟提取）

- **特点**: 本地运行，无需API密钥
- **用途**: 测试、演示、快速验证
- **性能**: 即时响应
- **准确性**: 基于规则的提取

```python
from fraud_detection.core import KeyIndicatorExtractor, ExtractorBackend

extractor = KeyIndicatorExtractor(backend=ExtractorBackend.MOCK)
indicators = extractor.extract_from_text(text, company_name)
```

**工作原理**:
- 文本关键词匹配
- 正则表达式数值提取
- 审计意见识别
- 情感分析（正面/负面关键词计数）
- 行业分类（关键词匹配）

### 2. Spark 后端（讯飞Spark LLM）

- **特点**: 国内LLM，支持中文
- **用途**: 生产环境，高准确性
- **性能**: 10-30秒
- **准确性**: LLM智能提取，高达95%+

**配置**:
```python
# 需要在环境变量或配置文件中设置
spark_config = {
    "spark_app_id": "your_app_id",
    "spark_api_key": "your_api_key",
    "spark_api_secret": "your_api_secret",
    "spark_api_url": "wss://spark-api.xf-yun.com/v4.0/chat"
}

extractor = KeyIndicatorExtractor(backend=ExtractorBackend.SPARK)
indicators = extractor.extract_from_text(text, company_name)
```

### 3. OpenAI 后端（GPT）

- **特点**: 国际通用，强大的语言理解
- **用途**: 生产环境，最高准确性
- **性能**: 10-30秒
- **准确性**: GPT-4级别，90%+

**配置**:
```python
import os
os.environ['OPENAI_API_KEY'] = 'your_api_key'

extractor = KeyIndicatorExtractor(backend=ExtractorBackend.OPENAI)
indicators = extractor.extract_from_text(text, company_name)
```

---

## 🚀 使用示例

### 示例 1: 从Apple财务报告提取

```python
from fraud_detection.core import KeyIndicatorExtractor

# Apple Q4 2024财务报告文本（示例）
apple_report = """
Apple Inc. Q4 2024 Financial Results
收入: $89.5B (环比增长5%)
净利润: $22.6B (利润率25%)
现金及等价物: $14.3B
自由现金流: $40.1B

Auditor Opinion: The financial statements present fairly...
(Unqualified Opinion)

Industry: Technology Hardware
Recent News: EU Antitrust Investigation, strong Vision Pro sales
"""

extractor = KeyIndicatorExtractor()
indicators = extractor.extract_from_text(apple_report, "Apple Inc.")

# 输出结果
print(f"公司: {indicators.extraction_source}")
print(f"收入: ${indicators.revenue:,.0f}")
print(f"净利润: ${indicators.net_income:,.0f}")
print(f"审计意见: {indicators.audit_opinion}")
print(f"行业: {indicators.industry_category}")
print(f"负面新闻数: {indicators.negative_news_count}")
print(f"置信度: {indicators.confidence_score:.2%}")

# JSON输出
import json
print(json.dumps(indicators.to_dict(), indent=2, ensure_ascii=False))
```

### 示例 2: 批量处理多个报告

```python
from fraud_detection.core import KeyIndicatorExtractor

# 多个公司的财务报告
companies_reports = [
    ("Apple Inc. financial report text...", "Apple Inc."),
    ("Microsoft financial report text...", "Microsoft"),
    ("Google financial report text...", "Alphabet Inc."),
]

extractor = KeyIndicatorExtractor()
all_results = extractor.batch_extract(companies_reports)

# 处理结果
for indicators in all_results:
    print(f"Company: {indicators.extraction_source}")
    print(f"Confidence: {indicators.confidence_score:.2%}")
    print(f"Revenue: {indicators.revenue}")
    print("-" * 50)
```

### 示例 3: REST API调用

```bash
# 单个报告提取
curl -X POST http://localhost:5000/api/extract/indicators \
  -H "Content-Type: application/json" \
  -d '{
    "text": "财务报告文本...",
    "company_name": "Apple Inc.",
    "backend": "mock"
  }'

# 响应示例
{
    "success": true,
    "company_name": "Apple Inc.",
    "indicators": {
        "revenue": 89500000000,
        "net_income": 22600000000,
        "audit_opinion": "Unqualified",
        "industry_category": "Technology",
        "tone_factor": "Positive",
        ...
    },
    "confidence_score": 0.85
}
```

---

## 🔌 API端点

### POST /api/extract/indicators
单个财务报告的指标提取

**请求**:
```json
{
    "text": "财务报告文本（必需）",
    "company_name": "公司名称（可选）",
    "backend": "mock|openai|spark（可选，默认mock）"
}
```

**响应**:
```json
{
    "success": true,
    "company_name": "Apple Inc.",
    "indicators": { ... },
    "confidence_score": 0.85
}
```

### POST /api/extract/indicators/batch
批量提取多个报告

**请求**:
```json
{
    "reports": [
        {"text": "报告1...", "company_name": "公司A"},
        {"text": "报告2...", "company_name": "公司B"}
    ],
    "backend": "mock"
}
```

**响应**:
```json
{
    "success": true,
    "total": 2,
    "successful": 2,
    "results": [ ... ]
}
```

### POST /api/extract/indicators/structured
从结构化数据提取

**请求**:
```json
{
    "financial_data": {
        "revenue": 1000000,
        "net_income": 100000,
        ...
    }
}
```

---

## 📈 置信度分数（Confidence Score）

置信度分数(0.0-1.0)反映提取结果的可靠性：

| 分数范围 | 含义 | 推荐行动 |
|---------|------|--------|
| 0.8-1.0 | 非常高 | 可直接使用 |
| 0.6-0.8 | 中等 | 建议人工验证 |
| 0.4-0.6 | 较低 | 需要人工审查 |
| 0.0-0.4 | 很低 | 不建议使用 |

---

## 🎓 最佳实践

### 1. 选择合适的后端

```python
# 快速测试 → 使用 MOCK
if is_testing:
    backend = ExtractorBackend.MOCK

# 生产环境，需要高准确性 → 使用 SPARK 或 OPENAI
elif requires_accuracy:
    backend = ExtractorBackend.OPENAI  # 或 SPARK
```

### 2. 处理低置信度结果

```python
indicators = extractor.extract_from_text(text, company_name)

if indicators.confidence_score < 0.7:
    logger.warning(f"Low confidence score: {indicators.confidence_score}")
    # 采用备选策略或人工审查
```

### 3. 错误处理

```python
try:
    indicators = extractor.extract_from_text(text, company_name)
except Exception as e:
    logger.error(f"Extraction failed: {e}")
    # 使用默认值或fallback
    indicators = ExtractedIndicators(confidence_score=0.0)
```

### 4. 性能优化

```python
# 批量处理比单个循环更高效
reports = [(text1, name1), (text2, name2), ...]
results = extractor.batch_extract(reports)
```

---

## 🔍 故障排除

### 问题 1: 置信度分数过低

**原因**:
- 报告格式特殊或不规范
- 缺少关键信息
- 使用的是MOCK后端

**解决方案**:
```python
# 尝试使用更强大的LLM后端
extractor = KeyIndicatorExtractor(backend=ExtractorBackend.OPENAI)
indicators = extractor.extract_from_text(text, company_name)
```

### 问题 2: 数值提取不准确

**原因**:
- 文本中数值格式特殊
- 存在多个相似的数值
- MOCK后端的局限性

**解决方案**:
```python
# 使用结构化数据提取
if has_structured_data:
    indicators = extractor.extract_from_structured_data(financial_data)
```

### 问题 3: API超时

**原因**:
- LLM服务响应慢
- 文本过长
- 网络连接问题

**解决方案**:
```python
# 减少文本长度，或使用异步处理
# 截断报告到关键部分
truncated_text = text[:5000]
indicators = extractor.extract_from_text(truncated_text, company_name)
```

---

## 📝 总结

`KeyIndicatorExtractor` 模块提供：
- ✅ 三种提取方式（文本、结构化、批量）
- ✅ 多个LLM后端支持
- ✅ 自动置信度评分
- ✅ 完整的错误处理
- ✅ RESTful API接口
- ✅ 高效的批处理

适合在金融数据处理、自动报表分析、投资决策支持等场景中使用。
