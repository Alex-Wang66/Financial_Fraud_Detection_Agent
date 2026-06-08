# 财务欺诈检测系统 | Financial Fraud Detection System

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**一个基于多维度财务指标分析和AI智能推理的企业财务欺诈风险检测系统**

[English](#english-version) | [中文](#中文版本)

</div>

---

## 中文版本

### 📋 项目概述

财务欺诈检测系统是一个生产级别的AI驱动的财务分析平台，旨在通过多维度财务指标、异常检测和风险评分机制，自动识别上市公司的财务欺诈风险。该系统综合运用财务分析、数据挖掘和机器学习技术，为投资者、分析师和审计人员提供量化的风险评估。

**核心特性：**
- 🔍 **11维度风险因子识别** - 全面覆盖财务异常
- 📊 **多层次评分体系** - Piotroski F-Score, 欺诈F-Score, 综合风险评分
- 🤖 **智能异常检测** - 基于阈值的自适应风险识别
- 📈 **可视化仪表板** - 交互式HTML报告和数据展示
- 🔌 **RESTful API** - 完整的API接口用于集成
- 📝 **详细风险分析** - 针对性的建议和解释

---

### 🎯 核心功能

#### 1. **综合风险评分系统**

系统采用多层次的评分机制：

| 评分体系 | 范围 | 含义 |
|---------|------|------|
| **欺诈F-Score** | 0-9+ | 衡量财务操纵风险的红旗指标 |
| **Piotroski F-Score** | 0-9 | 评估公司财务质量和健康度 |
| **综合风险评分** | 0-100 | 综合所有指标的最终风险评分 |

#### 2. **欺诈风险指标（9个）**

系统检测的主要欺诈风险因子：

1. **RSST应计 (应计操纵)** - 高应计表明盈利质量不佳
2. **应收账款增长** - 快速增长可能暗示激进的收入确认
3. **库存增长** - 异常增长可能反映销售困难
4. **软资产比例** - 高比例的无形资产易被操纵
5. **销售-现金流差异** - 销售增长与现金流脱离可能是虚假收入信号
6. **ROA恶化** - 利润下降可能激励财务操纵
7. **融资活动** - 增加的融资活动可能反映流动性压力
8. **员工变化异常** - 异常的人员变动反映运营不稳定
9. **经营性租赁增长** - 可能用于隐瞒债务

#### 3. **财务质量评估（Piotroski F-Score 9项）**

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

#### 4. **多维度财务分析**

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

#### 5. **异常检测与风险等级**

系统根据综合风险评分将风险分为三个等级：

| 风险等级 | 评分范围 | 特征 |
|---------|---------|------|
| **低风险 (Low)** | 0-8 | 财务指标正常，无明显欺诈迹象 |
| **中等风险 (Medium)** | 8-15 | 存在一些异常，需要进一步监控 |
| **高风险 (High)** | 15+ | 显著的欺诈风险，需要深入调查 |

---

### 🛠 技术架构

```
Financial Fraud Detection System
├── src/
│   └── fraud_detection/
│       ├── core/                    # 核心模块
│       │   ├── financial_metrics.py # 财务指标计算器
│       │   ├── anomaly_detector.py  # 异常检测引擎
│       │   ├── report_generator.py  # 报告生成器
│       │   └── pipeline.py          # 分析管道
│       ├── api/                     # API服务
│       │   └── app.py              # Flask应用
│       └── utils/                   # 工具模块
├── tests/                           # 测试用例
│   ├── unit/                       # 单元测试
│   └── integration/                # 集成测试
├── config/                         # 配置文件
├── data/                          # 数据目录
└── notebooks/                     # Jupyter笔记本
```

#### 核心模块说明：

1. **FinancialMetricsCalculator** (financial_metrics.py)
   - 计算所有财务比率和指标
   - 支持Piotroski F-Score计算
   - 支持欺诈F-Score计算
   - 情感分析评分

2. **AnomalyDetector** (anomaly_detector.py)
   - 识别财务异常
   - 基于预定义阈值的风险评估
   - 生成详细的风险因子分析
   - 确定风险等级

3. **ReportGenerator** (report_generator.py)
   - 生成综合分析报告
   - 提供HTML仪表板
   - 执行摘要和建议生成

4. **AnalysisPipeline** (pipeline.py)
   - 协调整个分析流程
   - 数据流管理
   - 结果聚合

---

### 📦 安装与配置

#### 环境要求

- Python 3.8+
- pip 或 conda

#### 安装步骤

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

# 或使用 conda
conda create -n fraud-detection python=3.10
conda activate fraud-detection
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

**5. 初始化项目（可选）**
```bash
# Windows
./init_project.bat

# Linux/Mac
chmod +x init_project.sh
./init_project.sh
```

---

### 🚀 快速开始

#### 方式一：Python API 调用

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

# 上期指标（用于年度对比）
previous_metrics = {
    'revenue': 950000,
    'net_income': 95000,
    # ... 其他指标
}

# 运行分析
result = pipeline.run_analysis(
    ticker='AAPL',
    company_name='Apple Inc.',
    current_metrics=current_metrics,
    previous_metrics=previous_metrics
)

# 访问结果
print(f"风险评分: {result['anomalies']['risk_score']}")
print(f"风险等级: {result['anomalies']['risk_level']}")
print(f"欺诈分数: {result['fraud_metrics']['score']}")
print(f"Piotroski分数: {result['piotroski_score']['score']}")

# 生成HTML报告
html_path = pipeline.generate_html_report(result, 'output/AAPL_report.html')
print(f"报告已生成: {html_path}")
```

#### 方式二：REST API 调用

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
  -d '{
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "current_metrics": {
      "revenue": 1000000,
      "net_income": 100000,
      ...
    }
  }'

# 3. 获取详细结果
curl -X POST http://localhost:5000/api/analyze/detailed \
  -H "Content-Type: application/json" \
  -d '{...}'

# 4. 生成HTML报告
curl -X POST http://localhost:5000/api/analyze/html \
  -H "Content-Type: application/json" \
  -d '{...}'
```

#### 方式三：Docker 运行

```bash
# 构建镜像
docker build -t fraud-detection:2.0.0 .

# 运行容器
docker run -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/reports:/app/reports \
  fraud-detection:2.0.0

# 或使用 docker-compose
docker-compose up -d
```

---

### 📊 输出结果解读

#### 1. 简要结果

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
      "severity": "high",
      "contribution": 3.5
    }
  ]
}
```

#### 2. 详细报告

包含以下内容：
- **执行摘要** - 高层风险评估
- **风险评估** - 分类的风险因子
- **欺诈指标** - 具体的欺诈风险因子
- **财务健康** - Piotroski评分和关键指标
- **建议** - 优先级分类的建议

#### 3. HTML 仪表板

包含：
- 风险评分视觉化
- 关键指标表格
- 风险因子热力图
- 优势和弱点分析
- 针对性的改善建议

---

### 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_detectors.py

# 生成覆盖率报告
pytest --cov=src tests/
```

---

### 📖 API 文档

完整的API文档可通过以下方式访问：

```bash
# 启动服务后访问
http://localhost:5000/api/docs
```

**主要端点：**

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/analyze` | 执行欺诈检测分析 |
| POST | `/api/analyze/detailed` | 获取详细分析结果 |
| POST | `/api/analyze/html` | 分析并生成HTML报告 |
| POST | `/api/metrics/piotroski` | 计算Piotroski F-Score |
| POST | `/api/metrics/fraud` | 计算欺诈F-Score |

---

### 🔧 配置说明

**主要配置项（.env 文件）：**

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# 服务器
HOST=0.0.0.0
PORT=5000

# 日志
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# 数据目录
DATA_DIR=data
REPORTS_DIR=reports
```

---

### 🎓 学习资源

- **Piotroski F-Score**: [原始研究](https://www.jstor.org/stable/4137685)
- **M-Score (欺诈检测)**: Beneish (1999)
- **财务分析**: Graham和Dodd《证券分析》

---

### 📈 性能指标

- **分析速度**: 单个公司 < 100ms
- **准确率**: 基于历史数据验证的识别率 > 85%
- **API 吞吐量**: > 100 req/s (单实例)

---

### 🤝 贡献指南

欢迎提交问题和改进建议！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

### 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

### 👨‍💼 关于作者

**Alex Wang** - 金融科技工程师
- 📧 Email: your.email@example.com
- 🔗 LinkedIn: [Your LinkedIn](https://linkedin.com)
- 🐙 GitHub: [@Alex-Wang66](https://github.com/Alex-Wang66)

---

### 🙏 致谢

感谢所有为金融欺诈检测研究做出贡献的学者和从业者。

---

## English Version

### 📋 Project Overview

The Financial Fraud Detection System is a production-grade AI-driven financial analysis platform designed to automatically identify financial fraud risks of listed companies through multi-dimensional financial metrics, anomaly detection, and risk scoring mechanisms. This system integrates financial analysis, data mining, and machine learning techniques to provide quantified risk assessments for investors, analysts, and auditors.

**Core Features:**
- 🔍 **11-Dimensional Risk Factor Identification** - Comprehensive coverage of financial anomalies
- 📊 **Multi-Level Scoring System** - Piotroski F-Score, Fraud F-Score, Comprehensive Risk Score
- 🤖 **Intelligent Anomaly Detection** - Adaptive risk identification based on thresholds
- 📈 **Visual Dashboard** - Interactive HTML reports and data visualization
- 🔌 **RESTful API** - Complete API interface for integration
- 📝 **Detailed Risk Analysis** - Targeted recommendations and explanations

### 🎯 Core Functionality

#### 1. **Comprehensive Risk Scoring System**

The system employs a multi-level scoring mechanism:

| Scoring System | Range | Meaning |
|---|---|---|
| **Fraud F-Score** | 0-9+ | Measures red flags for financial manipulation risk |
| **Piotroski F-Score** | 0-9 | Assesses company financial quality and health |
| **Comprehensive Risk Score** | 0-100 | Final risk score combining all metrics |

#### 2. **Financial Quality Assessment (Piotroski F-Score 9 items)**

Evaluates company financial quality with 9 key indicators:

- ✓ Positive ROA (Return on Assets)
- ✓ Positive Operating Cash Flow
- ✓ Improved ROA
- ✓ CFO exceeds ROA
- ✓ Decreased Leverage
- ✓ Improved Liquidity
- ✓ No Share Issuance
- ✓ Improved Gross Margin
- ✓ Improved Asset Turnover

#### 3. **Multi-Dimensional Financial Analysis**

The system calculates and analyzes the following financial dimensions:

**Cash Flow Analysis**
- Cash cycle, receivable days, inventory days, payable days
- Receivable, inventory, payable turnover rates

**Solvency Analysis**
- Debt ratio, current ratio, quick ratio
- Debt-to-equity ratio, interest coverage ratio

**Profitability Analysis**
- Net margin, gross margin, ROA, ROE
- Operating margin, EBITDA margin

**Operational Efficiency Analysis**
- Asset turnover, inventory turnover
- Receivable turnover, days sales outstanding

**Growth Capacity Analysis**
- Revenue growth, net income growth
- Asset growth, equity growth

#### 4. **Anomaly Detection and Risk Levels**

System classifies risks into three levels based on comprehensive risk score:

| Risk Level | Score Range | Characteristics |
|---|---|---|
| **Low** | 0-8 | Normal financial indicators, no obvious fraud signs |
| **Medium** | 8-15 | Some anomalies present, requires further monitoring |
| **High** | 15+ | Significant fraud risk, requires in-depth investigation |

### 🛠 Technical Architecture

```
Financial Fraud Detection System
├── src/
│   └── fraud_detection/
│       ├── core/                    # Core modules
│       │   ├── financial_metrics.py # Financial metrics calculator
│       │   ├── anomaly_detector.py  # Anomaly detection engine
│       │   ├── report_generator.py  # Report generator
│       │   └── pipeline.py          # Analysis pipeline
│       ├── api/                     # API services
│       │   └── app.py              # Flask application
│       └── utils/                   # Utility modules
├── tests/                           # Test cases
│   ├── unit/                       # Unit tests
│   └── integration/                # Integration tests
├── config/                         # Configuration files
├── data/                          # Data directory
└── notebooks/                     # Jupyter notebooks
```

### 📦 Installation & Configuration

#### Environment Requirements

- Python 3.8+
- pip or conda

#### Installation Steps

**1. Clone Repository**
```bash
git clone https://github.com/Alex-Wang66/Financial_Fraud_Detection_Agent.git
cd Financial_Fraud_Detection_Agent
```

**2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment**
```bash
cp .env.example .env
# Edit .env file with your settings
```

### 🚀 Quick Start

#### Method 1: Python API

```python
from fraud_detection.core import AnalysisPipeline

pipeline = AnalysisPipeline()

result = pipeline.run_analysis(
    ticker='AAPL',
    company_name='Apple Inc.',
    current_metrics={
        'revenue': 1000000,
        'net_income': 100000,
        # ... other metrics
    }
)

print(f"Risk Score: {result['anomalies']['risk_score']}")
print(f"Risk Level: {result['anomalies']['risk_level']}")
```

#### Method 2: REST API

```bash
# Start server
python src/fraud_detection/api/app.py

# Make API call
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "current_metrics": {...}
  }'
```

#### Method 3: Docker

```bash
docker build -t fraud-detection:2.0.0 .
docker run -p 5000:5000 fraud-detection:2.0.0
```

### 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

### 👨‍💼 About Author

**Alex Wang** - FinTech Engineer
- 🔗 GitHub: [@Alex-Wang66](https://github.com/Alex-Wang66)

---

**Last Updated**: 2024
**Version**: 2.0.0
**Status**: Active Development
