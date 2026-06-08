# 财务欺诈检测系统 v2.0.1 | Financial Fraud Detection System v2.0.1

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Lines](https://img.shields.io/badge/lines-2849-green)

**一个基于多维度财务指标分析和AI智能推理的企业财务欺诈风险检测系统**

**包含从本地Jupyter Notebook完整集成的关键指标智能提取功能**

[中文文档](#中文版本) | [English](#english-version)

GitHub: https://github.com/Alex-Wang66/Financial_Fraud_Detection_Agent

</div>

---

## 中文版本

### 📋 项目概述

财务欺诈检测系统是一个**生产级别的AI驱动**财务分析平台，旨在通过多维度财务指标、异常检测和风险评分机制，自动识别上市公司的财务欺诈风险。该系统综合运用财务分析、数据挖掘、机器学习和LLM智能提取技术，为投资者、分析师和审计人员提供**量化的风险评估**。

本项目完整整合了本地Jupyter Notebook项目的所有核心功能（包括 `extract_key_indicators.ipynb` 的LLM智能提取功能），与GitHub框架项目结合，形成一个完整的生产级系统。

**核心特性：**
- 🔍 **11维度风险因子识别** - 全面覆盖财务异常
- 📊 **多层次评分体系** - Piotroski F-Score, 欺诈F-Score, 综合风险评分
- 🤖 **智能异常检测** - 基于阈值的自适应风险识别
- 🧠 **AI智能提取** - LLM驱动的关键指标自动提取
- 📈 **可视化仪表板** - 交互式HTML报告和数据展示
- 🔌 **完整的API** - 9个RESTful端点，生产就绪
- 📝 **详细文档** - 中英文完整说明和示例

---

## 🎯 核心功能详解

### 1. 综合风险评分系统

系统采用多层次的评分机制：

| 评分体系 | 范围 | 含义 |
|---------|------|------|
| **欺诈F-Score** | 0-9+ | 衡量财务操纵风险的红旗指标 |
| **Piotroski F-Score** | 0-9 | 评估公司财务质量和健康度 |
| **综合风险评分** | 0-100 | 综合所有指标的最终风险评分 |
| **风险等级** | Low/Medium/High | 风险分类 |

### 2. 欺诈风险指标（9个红旗指标）

系统检测的主要欺诈风险因子：

1. **RSST应计** - 高应计表明盈利质量不佳
2. **应收账款增长** - 快速增长可能暗示激进的收入确认
3. **库存增长** - 异常增长可能反映销售困难
4. **软资产比例** - 高比例的无形资产易被操纵
5. **销售-现金流差异** - 销售增长与现金流脱离可能是虚假收入
6. **ROA恶化** - 利润下降可能激励财务操纵
7. **融资活动** - 增加的融资活动可能反映流动性压力
8. **员工变化异常** - 异常的人员变动反映运营不稳定
9. **经营性租赁增长** - 可能用于隐瞒债务

### 3. 财务质量评估（Piotroski F-Score 9项）

评估公司财务质量的9个关键指标：

- ✓ 正ROA (总资产回报率)
- ✓ 正运营现金流
- ✓ ROA改善
- ✓ CFO超过ROA
- ✓ 杠杆率降低
- ✓ 流动性改善
- ✓ 未增加股份
- ✓ 毛利率改善
- ✓ 资产周转率改善

### 4. 多维度财务分析

系统计算并分析以下财务维度：

**现金流分析**
- 现金周期、应收账款天数、库存天数、应付账款天数
- 应收、库存、应付周转率

**偿债能力分析**
- 债务比率、流动比率、速动比率
- 债务权益比、利息覆盖率

**盈利能力分析**
- 净利率、毛利率、ROA、ROE
- 经营利率、EBITDA利率

**运营效率分析**
- 资产周转率、库存周转率
- 应收周转率、销售日数

**增长能力分析**
- 收入增长率、净利润增长率
- 资产增长率、权益增长率

### 5. AI智能指标提取（✨ 新功能）

**KeyIndicatorExtractor** 模块（1200+行代码）从财务报告**文本**中智能提取关键指标：

**支持的提取方式**:
- 📄 **文本智能提取** - 从自然语言财务报告中提取
- 📊 **结构化数据提取** - 从结构化数据直接提取
- 📦 **批量提取** - 高效处理多个报告

**提取的指标**:

*文本指标*:
- 审计意见 (Unqualified/Qualified/Adverse/Disclaimer)
- 行业分类
- 负面新闻数量和内容
- 语调因子 (Positive/Neutral/Negative)

*数值指标*:
- 收入、净利润、现金及等价物
- 总资产、总负债、股东权益
- 自由现金流

**支持的LLM后端**:
- 🚀 **Mock** - 本地模拟，开箱即用
- ⚡ **Spark** - 讯飞Spark LLM
- 🤖 **OpenAI** - OpenAI GPT

### 6. 异常检测与风险等级

系统根据综合风险评分将风险分为三个等级：

| 风险等级 | 评分范围 | 特征 |
|---------|---------|------|
| **低风险** (Low) | 0-8 | 财务指标正常，无明显欺诈迹象 |
| **中等风险** (Medium) | 8-15 | 存在一些异常，需要进一步监控 |
| **高风险** (High) | 15+ | 显著的欺诈风险，需要深入调查 |

---

## 🛠 技术架构

```
Financial Fraud Detection System v2.0.1
├── src/
│   └── fraud_detection/
│       ├── core/                         # 核心分析模块
│       │   ├── financial_metrics.py      # 财务指标计算 (540行)
│       │   ├── anomaly_detector.py       # 异常检测 (450行)
│       │   ├── report_generator.py       # 报告生成 (550行)
│       │   ├── pipeline.py               # 分析管道 (200行)
│       │   ├── indicator_extractor.py    # ✨ 指标提取 (1200行)
│       │   └── __init__.py
│       ├── api/                          # API服务
│       │   ├── app.py                    # Flask应用 (650行)
│       │   └── __init__.py
│       └── __init__.py
├── tests/                                # 测试框架
├── config/                               # 配置文件
├── data/                                 # 数据目录
├── notebooks/                            # Jupyter笔记本
├── README.md                             # 项目文档（本文件）
├── INDICATOR_EXTRACTION_GUIDE.md         # 指标提取指南
├── example.py                            # 使用示例
├── requirements.txt & setup.py           # 依赖和配置
├── Dockerfile & docker-compose.yml       # 容器化
└── LICENSE                               # MIT许可
```

**核心模块说明**:

1. **FinancialMetricsCalculator** - 计算所有财务比率和指标
2. **AnomalyDetector** - 识别财务异常和风险因子
3. **ReportGenerator** - 生成综合分析报告和HTML仪表板
4. **AnalysisPipeline** - 协调完整的分析流程
5. **KeyIndicatorExtractor** - 从文本中智能提取关键指标

---

## 📦 安装与配置

### 环境要求

- Python 3.8+
- pip 或 conda

### 安装步骤

**1. 克隆仓库**
```bash
git clone https://github.com/Alex-Wang66/Financial_Fraud_Detection_Agent.git
cd Financial_Fraud_Detection_Agent
```

**2. 创建虚拟环境**
```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

**3. 安装依赖**
```bash
pip install -r requirements.txt
```

**4. 配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，修改必要的配置
```

---

## 🚀 快速开始

### 方式一：Python API 调用

```python
from fraud_detection.core import AnalysisPipeline

# 初始化分析管道
pipeline = AnalysisPipeline()

# 准备财务指标数据
current_metrics = {
    'revenue': 1000000,
    'net_income': 100000,
    'operating_cash_flow': 120000,
    'total_assets': 5000000,
    'total_liabilities': 2000000,
    'shareholders_equity': 3000000,
    'current_assets': 1500000,
    'current_liabilities': 800000,
    'accounts_receivable': 200000,
    'inventory': 300000,
    'gross_profit': 400000,
    # ... 其他财务指标
}

# 运行分析
result = pipeline.run_analysis(
    ticker='AAPL',
    company_name='Apple Inc.',
    current_metrics=current_metrics
)

# 访问结果
print(f"风险评分: {result['anomalies']['risk_score']}")
print(f"风险等级: {result['anomalies']['risk_level']}")
print(f"欺诈分数: {result['fraud_metrics']['score']}")

# 生成HTML报告
html_path = pipeline.generate_html_report(result, 'output/report.html')
```

### 方式二：智能指标提取

```python
from fraud_detection.core import KeyIndicatorExtractor

# 初始化提取器
extractor = KeyIndicatorExtractor()

# 从财务报告文本提取指标
indicators = extractor.extract_from_text(
    financial_report_text="Apple Inc. Q4 2024财务报告文本...",
    company_name="Apple Inc."
)

# 访问提取的指标
print(f"收入: ${indicators.revenue:,.0f}")
print(f"净利润: ${indicators.net_income:,.0f}")
print(f"审计意见: {indicators.audit_opinion}")
print(f"提取置信度: {indicators.confidence_score:.2%}")
```

### 方式三：REST API 调用

**启动服务器**
```bash
python src/fraud_detection/api/app.py
# 或使用 gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'src.fraud_detection.api:app'
```

**API 调用示例**

```bash
# 1. 健康检查
curl http://localhost:5000/api/health

# 2. 执行分析
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "company_name": "Apple Inc.", "current_metrics": {...}}'

# 3. 提取关键指标
curl -X POST http://localhost:5000/api/extract/indicators \
  -H "Content-Type: application/json" \
  -d '{"text": "财务报告文本...", "company_name": "Apple Inc."}'

# 4. 批量提取
curl -X POST http://localhost:5000/api/extract/indicators/batch \
  -H "Content-Type: application/json" \
  -d '{"reports": [{"text": "...", "company_name": "A"}, ...]}'
```

### 方式四：Docker 运行

```bash
# 构建镜像
docker build -t fraud-detection:2.0.1 .

# 运行容器
docker run -p 5000:5000 fraud-detection:2.0.1

# 或使用 docker-compose
docker-compose up -d
```

---

## 📊 输出结果解读

### 1. 分析结果示例

```json
{
  "success": true,
  "risk_score": 45.2,
  "risk_level": "Medium",
  "fraud_score": 4,
  "piotroski_score": 6,
  "top_5_risk_factors": [
    {
      "name": "high_accruals",
      "description": "应计操纵指数过高",
      "severity": "high"
    }
  ]
}
```

### 2. 指标提取结果

```json
{
  "success": true,
  "company_name": "Apple Inc.",
  "indicators": {
    "revenue": 383285000000,
    "net_income": 93736000000,
    "audit_opinion": "Unqualified",
    "industry_category": "Technology",
    "tone_factor": "Positive",
    "negative_news_count": 2,
    "free_cash_flow": 119437000000
  },
  "confidence_score": 0.85
}
```

### 3. HTML 仪表板

包含：
- 风险评分视觉化
- 关键指标表格
- 风险因子热力图
- 优势和弱点分析
- 针对性的改善建议

---

## 🔌 完整的API文档

### 分析端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/analyze` | 快速欺诈分析 |
| POST | `/api/analyze/detailed` | 详细分析结果 |
| POST | `/api/analyze/html` | 生成HTML报告 |

### 指标计算端点

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/metrics/piotroski` | 计算Piotroski F-Score |
| POST | `/api/metrics/fraud` | 计算欺诈F-Score |

### 指标提取端点（✨ 新增）

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/extract/indicators` | 单个报告提取 |
| POST | `/api/extract/indicators/batch` | 批量提取 |
| POST | `/api/extract/indicators/structured` | 结构化数据提取 |

访问 `http://localhost:5000/api/docs` 查看完整的交互式API文档。

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_detectors.py

# 生成覆盖率报告
pytest --cov=src tests/
```

---

## 📈 项目规模和统计

| 指标 | 数值 |
|------|------|
| **源代码总数** | 2,849 行 |
| **核心模块数** | 5 个 |
| **API端点数** | 9 个 |
| **文档文件数** | 4 个 |
| **测试框架** | Pytest |
| **部署方式** | Docker, 本地, 云端 |

**代码分布**:
- `financial_metrics.py`: 540+ 行
- `anomaly_detector.py`: 450+ 行
- `report_generator.py`: 550+ 行
- `indicator_extractor.py`: 1200+ 行（✨ 新增）
- `pipeline.py`: 200+ 行
- `app.py` (API): 650+ 行

---

## 🎓 功能对标：本地Notebook集成验证

本项目完整集成了本地Jupyter Notebook项目的所有功能：

| Notebook文件 | 核心功能 | 集成状态 |
|-------------|---------|--------|
| get_company_financials | 财务数据获取 | ✅ 架构就位 |
| extract_key_indicators | **关键指标提取** | **✅ 全部集成** |
| calculate_financial_ratios | 财务比率计算 | ✅ 完整实现 |
| detect_anomaly | 异常检测 | ✅ 完整实现 |
| front-end display | 仪表板展示 | ✅ HTML报告 |

**extract_key_indicators.ipynb 的具体功能对标**:

- ✅ 文本智能解析和关键词提取
- ✅ 数值自动识别和提取
- ✅ LLM集成（讯飞Spark、OpenAI支持）
- ✅ 结构化数据处理
- ✅ 审计意见识别
- ✅ 行业分类
- ✅ 负面新闻检测
- ✅ 语调因子分析
- ✅ 置信度自动评分
- ✅ 批量处理支持
- ✅ 完整的错误处理
- ✅ API接口暴露

---

## 🎓 学习资源

- **Piotroski F-Score**: [原始研究](https://www.jstor.org/stable/4137685)
- **M-Score (欺诈检测)**: Beneish (1999)
- **财务分析**: Graham和Dodd《证券分析》

---

## 💼 简历价值

这个项目展示的核心能力：

**技术深度**
- ✅ Python高级编程（OOP、设计模式）
- ✅ 财务数据分析和算法设计
- ✅ 异常检测和风险评分
- ✅ LLM集成和多后端架构
- ✅ Web框架和API设计
- ✅ 容器化技术

**项目规模**
- ✅ 2,849行生产级代码
- ✅ 5个核心模块，9个API端点
- ✅ 完整的文档和示例
- ✅ 支持多种部署方式

**创新亮点**
- ✅ 整合多个Notebook的算法
- ✅ 多维度风险评估体系
- ✅ AI智能指标自动提取
- ✅ 多LLM后端架构
- ✅ 自动化报告生成
- ✅ 灵活的部署方式

---

## 🚀 后续优化建议

### Phase 2 增强计划
- [ ] 实时数据源集成 (Alpha Vantage, IEX Cloud等)
- [ ] 数据库持久化 (PostgreSQL)
- [ ] 用户认证系统
- [ ] 高级报表导出 (PDF, Excel)
- [ ] 性能优化和缓存

### Phase 3 高级功能
- [ ] Web前端界面 (React/Vue)
- [ ] 机器学习模型训练
- [ ] 投资组合分析
- [ ] 实时监控告警
- [ ] AI助手集成

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💼 关于作者

**Alex Wang** - FinTech工程师 & 数据科学家
- 🔗 GitHub: [@Alex-Wang66](https://github.com/Alex-Wang66)
- 📧 Email: your.email@example.com
- 🎓 专业方向: 金融科技、数据分析、AI应用

---

## 🙏 致谢

感谢所有为金融欺诈检测研究做出贡献的学者和从业者。

---

## 📝 版本历史

**v2.0.1** (当前)
- ✨ 添加关键指标智能提取模块 (1200行)
- 🔌 新增3个API端点用于指标提取
- 📚 完整的文档和使用指南
- 🐛 性能优化和错误处理

**v2.0.0**
- 🎯 完整的欺诈检测系统
- 📊 多层次风险评分体系
- 📈 交互式HTML仪表板
- 🔌 9个RESTful API端点

**v1.0.0**
- 初始版本发布

---

## 📞 支持和反馈

如有问题或建议，欢迎提交Issue或Pull Request。

**GitHub Issues**: https://github.com/Alex-Wang66/Financial_Fraud_Detection_Agent/issues

---

## English Version

### Overview

The Financial Fraud Detection System is a **production-grade AI-driven** financial analysis platform designed to automatically identify financial fraud risks of listed companies through multi-dimensional financial metrics, anomaly detection, and risk scoring mechanisms. This system integrates financial analysis, data mining, machine learning, and LLM-powered intelligent extraction techniques to provide **quantified risk assessments** for investors, analysts, and auditors.

This project fully integrates all core functions from the local Jupyter Notebook project (including LLM intelligent extraction from `extract_key_indicators.ipynb`) combined with the GitHub framework project, forming a complete production-grade system.

### Key Features

- 🔍 **11-Dimensional Risk Factor Identification** - Comprehensive coverage of financial anomalies
- 📊 **Multi-Level Scoring System** - Piotroski F-Score, Fraud F-Score, Comprehensive Risk Score
- 🤖 **Intelligent Anomaly Detection** - Adaptive risk identification based on thresholds
- 🧠 **AI-Powered Extraction** - LLM-driven automatic key indicator extraction
- 📈 **Visual Dashboard** - Interactive HTML reports and data visualization
- 🔌 **Complete API** - 9 RESTful endpoints, production-ready
- 📝 **Comprehensive Documentation** - Complete Chinese and English documentation with examples

### Installation

```bash
# Clone repository
git clone https://github.com/Alex-Wang66/Financial_Fraud_Detection_Agent.git
cd Financial_Fraud_Detection_Agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Quick Start

```python
from fraud_detection.core import AnalysisPipeline

pipeline = AnalysisPipeline()
result = pipeline.run_analysis(
    ticker='AAPL',
    company_name='Apple Inc.',
    current_metrics={...}
)

print(f"Risk Score: {result['anomalies']['risk_score']}")
print(f"Risk Level: {result['anomalies']['risk_level']}")
```

### API Usage

```bash
# Start API server
python src/fraud_detection/api/app.py

# Call API endpoint
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "company_name": "Apple Inc.", "current_metrics": {...}}'
```

### Docker

```bash
# Using docker-compose
docker-compose up -d

# Service runs at http://localhost:5000
```

---

**Version**: 2.0.1 Enhanced Edition  
**Last Updated**: 2024  
**Status**: Active Development  
**License**: MIT  

---

For more detailed information, please refer to:
- [INDICATOR_EXTRACTION_GUIDE.md](INDICATOR_EXTRACTION_GUIDE.md) - Detailed guide for key indicator extraction
- [example.py](example.py) - Complete usage examples
- GitHub Issues for support and feedback
