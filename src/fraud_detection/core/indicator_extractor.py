"""
Key Indicators Extractor using LLM
关键指标提取模块（使用LLM智能提取）
"""

import logging
import json
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ExtractorBackend(Enum):
    """支持的LLM后端"""
    MOCK = "mock"  # 模拟模式（不需要API密钥）
    OPENAI = "openai"
    SPARK = "spark"  # 讯飞Spark API
    CUSTOM = "custom"


@dataclass
class ExtractedIndicators:
    """提取的关键指标数据类"""
    # 文本指标
    audit_opinion: Optional[str] = None  # 审计意见
    industry_category: Optional[str] = None  # 行业分类
    negative_news_count: int = 0  # 负面新闻数量
    negative_news_items: List[str] = None  # 具体负面新闻
    tone_factor: Optional[str] = None  # 语调因子 (Positive/Neutral/Negative)

    # 数值指标
    revenue: Optional[float] = None  # 收入
    net_income: Optional[float] = None  # 净利润
    cash_and_equivalents: Optional[float] = None  # 现金及等价物
    total_assets: Optional[float] = None  # 总资产
    total_liabilities: Optional[float] = None  # 总负债
    shareholders_equity: Optional[float] = None  # 股东权益
    free_cash_flow: Optional[float] = None  # 自由现金流

    # 提取元数据
    extraction_source: Optional[str] = None  # 提取来源
    confidence_score: float = 0.0  # 置信度分数 (0-1)
    extraction_timestamp: Optional[str] = None  # 提取时间戳
    raw_text_snippet: Optional[str] = None  # 原始文本片段

    def __post_init__(self):
        if self.negative_news_items is None:
            self.negative_news_items = []

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class KeyIndicatorExtractor:
    """关键指标提取器 - 使用LLM从财务文本中提取指标"""

    def __init__(self, backend: ExtractorBackend = ExtractorBackend.MOCK):
        """
        初始化提取器

        Args:
            backend: LLM后端类型
        """
        self.backend = backend
        self.extractor = self._initialize_backend()

    def _initialize_backend(self):
        """初始化LLM后端"""
        if self.backend == ExtractorBackend.MOCK:
            return MockExtractor()
        elif self.backend == ExtractorBackend.SPARK:
            return SparkExtractor()
        elif self.backend == ExtractorBackend.OPENAI:
            return OpenAIExtractor()
        else:
            logger.warning("Using mock extractor as fallback")
            return MockExtractor()

    def extract_from_text(
        self,
        financial_report_text: str,
        company_name: Optional[str] = None
    ) -> ExtractedIndicators:
        """
        从财务报告文本中提取关键指标

        Args:
            financial_report_text: 财务报告文本
            company_name: 公司名称（可选）

        Returns:
            提取的指标数据
        """
        logger.info(f"Extracting indicators from financial report ({len(financial_report_text)} chars)")

        try:
            # 使用配置的后端进行提取
            indicators = self.extractor.extract(financial_report_text, company_name)

            # 后处理和验证
            indicators = self._post_process(indicators)
            indicators.extraction_source = self.backend.value
            indicators.confidence_score = self._calculate_confidence(indicators)

            logger.info(f"Successfully extracted indicators. Confidence: {indicators.confidence_score:.2f}")
            return indicators

        except Exception as e:
            logger.error(f"Error extracting indicators: {str(e)}")
            # 返回空的指标对象作为fallback
            return ExtractedIndicators(confidence_score=0.0)

    def extract_from_structured_data(
        self,
        financial_data: Dict[str, Any]
    ) -> ExtractedIndicators:
        """
        从结构化财务数据中提取指标

        Args:
            financial_data: 结构化财务数据字典

        Returns:
            提取的指标
        """
        logger.info("Extracting indicators from structured data")

        indicators = ExtractedIndicators()

        # 数值字段映射
        numeric_mappings = {
            'revenue': ['revenue', 'totalRevenue', 'sales', 'income'],
            'net_income': ['netIncome', 'net_profit', 'net_earnings'],
            'cash_and_equivalents': ['cash', 'cashEquivalents', 'cash_and_equivalents'],
            'total_assets': ['totalAssets', 'assets'],
            'total_liabilities': ['totalLiabilities', 'liabilities'],
            'shareholders_equity': ['shareholdersEquity', 'equity', 'stockholdersEquity'],
            'free_cash_flow': ['freeCashFlow', 'fcf', 'free_cash_flow'],
        }

        # 提取数值指标
        for field, keys in numeric_mappings.items():
            for key in keys:
                if key in financial_data:
                    setattr(indicators, field, float(financial_data[key]))
                    break

        # 提取文本指标
        indicators.audit_opinion = financial_data.get('audit_opinion')
        indicators.industry_category = financial_data.get('industry_category')
        indicators.negative_news_count = len(
            financial_data.get('negative_news_items', [])
        )
        indicators.negative_news_items = financial_data.get('negative_news_items', [])
        indicators.tone_factor = financial_data.get('tone_factor')

        indicators.extraction_source = 'structured_data'
        indicators.confidence_score = self._calculate_confidence(indicators)

        return indicators

    def batch_extract(
        self,
        reports: List[Tuple[str, Optional[str]]]
    ) -> List[ExtractedIndicators]:
        """
        批量提取多个财务报告的指标

        Args:
            reports: 报告文本和公司名称的列表

        Returns:
            提取结果列表
        """
        logger.info(f"Batch extracting from {len(reports)} reports")

        results = []
        for text, company_name in reports:
            try:
                indicators = self.extract_from_text(text, company_name)
                results.append(indicators)
            except Exception as e:
                logger.error(f"Error extracting {company_name}: {str(e)}")
                results.append(ExtractedIndicators(confidence_score=0.0))

        return results

    def _post_process(self, indicators: ExtractedIndicators) -> ExtractedIndicators:
        """后处理提取的指标"""

        # 验证数值字段
        numeric_fields = [
            'revenue', 'net_income', 'cash_and_equivalents',
            'total_assets', 'total_liabilities', 'shareholders_equity',
            'free_cash_flow'
        ]

        for field in numeric_fields:
            value = getattr(indicators, field)
            if value is not None and value < 0:
                logger.warning(f"Negative value for {field}: {value}")

        # 验证审计意见
        valid_opinions = [
            'Unqualified', 'Qualified', 'Adverse', 'Disclaimer', 'Emphasis'
        ]
        if indicators.audit_opinion and indicators.audit_opinion not in valid_opinions:
            logger.warning(f"Unusual audit opinion: {indicators.audit_opinion}")

        # 验证语调因子
        valid_tones = ['Positive', 'Neutral', 'Negative']
        if indicators.tone_factor and indicators.tone_factor not in valid_tones:
            logger.warning(f"Unusual tone factor: {indicators.tone_factor}")

        return indicators

    def _calculate_confidence(self, indicators: ExtractedIndicators) -> float:
        """
        计算提取结果的置信度

        Args:
            indicators: 提取的指标

        Returns:
            置信度分数 (0-1)
        """
        score = 0.0
        checks = 0

        # 检查文本字段
        if indicators.audit_opinion:
            score += 0.1
        if indicators.industry_category:
            score += 0.1
        if indicators.tone_factor:
            score += 0.05

        checks += 3

        # 检查数值字段
        numeric_fields = [
            'revenue', 'net_income', 'cash_and_equivalents',
            'total_assets', 'total_liabilities', 'shareholders_equity',
            'free_cash_flow'
        ]

        for field in numeric_fields:
            if getattr(indicators, field) is not None:
                score += 0.1
            checks += 0.1

        # 检查负面新闻
        if indicators.negative_news_count > 0:
            score += min(0.05, indicators.negative_news_count * 0.02)

        # 正规化置信度分数
        if checks > 0:
            confidence = min(score, 1.0)
        else:
            confidence = 0.0

        return confidence


class MockExtractor:
    """模拟提取器 - 用于测试和演示"""

    def extract(
        self,
        text: str,
        company_name: Optional[str] = None
    ) -> ExtractedIndicators:
        """模拟提取逻辑"""

        indicators = ExtractedIndicators()

        # 尝试从文本中提取数值
        indicators.revenue = self._extract_number(text, ['revenue', 'total revenue'])
        indicators.net_income = self._extract_number(text, ['net income', 'net profit'])
        indicators.free_cash_flow = self._extract_number(text, ['free cash flow', 'fcf'])
        indicators.cash_and_equivalents = self._extract_number(text, ['cash', 'cash equivalents'])

        # 检测审计意见
        audit_keywords = {
            'Unqualified': ['unqualified', 'clean opinion', 'fair presentation'],
            'Qualified': ['qualified', 'except for', 'exception'],
            'Adverse': ['adverse', 'does not present fairly'],
            'Disclaimer': ['disclaimer', 'unable to', 'cannot express']
        }

        for opinion, keywords in audit_keywords.items():
            if any(kw in text.lower() for kw in keywords):
                indicators.audit_opinion = opinion
                break

        # 检测语调
        negative_words = ['risk', 'decline', 'loss', 'challenge', 'negative']
        positive_words = ['growth', 'profit', 'increase', 'strong', 'positive']

        negative_count = sum(text.lower().count(word) for word in negative_words)
        positive_count = sum(text.lower().count(word) for word in positive_words)

        if negative_count > positive_count:
            indicators.tone_factor = 'Negative'
        elif positive_count > negative_count:
            indicators.tone_factor = 'Positive'
        else:
            indicators.tone_factor = 'Neutral'

        # 检测负面新闻
        risk_keywords = ['risk', 'fraud', 'lawsuit', 'investigation', 'violation']
        indicators.negative_news_count = sum(
            text.lower().count(kw) for kw in risk_keywords
        )

        # 行业分类
        industry_keywords = {
            'Technology': ['tech', 'software', 'digital', 'it', 'chip'],
            'Finance': ['bank', 'financial', 'insurance', 'investment'],
            'Healthcare': ['pharma', 'healthcare', 'medical', 'hospital'],
            'Manufacturing': ['manufacture', 'industry', 'production'],
            'Energy': ['oil', 'gas', 'energy', 'power'],
        }

        for industry, keywords in industry_keywords.items():
            if any(kw in text.lower() for kw in keywords):
                indicators.industry_category = industry
                break

        return indicators

    def _extract_number(self, text: str, keywords: List[str]) -> Optional[float]:
        """从文本中提取与关键词相关的数值"""
        for keyword in keywords:
            # 查找关键词后的数值
            pattern = rf'{keyword}[:\s]*[\$]*([0-9,]+(?:\.[0-9]+)?)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    value_str = match.group(1).replace(',', '')
                    return float(value_str)
                except ValueError:
                    continue
        return None


class SparkExtractor:
    """讯飞Spark API提取器"""

    def __init__(self):
        """初始化Spark提取器"""
        try:
            from langchain_community.chat_models import ChatSparkLLM
            self.available = True
        except ImportError:
            logger.warning("langchain_community not installed, using mock extractor")
            self.available = False
            self.mock_extractor = MockExtractor()

    def extract(
        self,
        text: str,
        company_name: Optional[str] = None
    ) -> ExtractedIndicators:
        """使用Spark API提取指标"""

        if not self.available:
            logger.warning("Using mock extractor as fallback")
            return self.mock_extractor.extract(text, company_name)

        try:
            # 构建提取提示
            extraction_prompt = self._build_prompt(text, company_name)

            # 调用Spark API（需要配置API密钥）
            indicators = self._call_spark_api(extraction_prompt)
            return indicators

        except Exception as e:
            logger.error(f"Spark extraction failed: {str(e)}, using mock extractor")
            return self.mock_extractor.extract(text, company_name)

    def _build_prompt(self, text: str, company_name: Optional[str]) -> str:
        """构建LLM提示"""
        prompt = f"""
从以下财务报告中提取关键指标，返回JSON格式：

{text[:2000]}  # 限制文本长度以节省tokens

提取以下信息：
1. 审计意见 (audit_opinion): Unqualified/Qualified/Adverse/Disclaimer
2. 行业分类 (industry_category):
3. 负面新闻数量和列表 (negative_news_count, negative_news_items):
4. 语调因子 (tone_factor): Positive/Neutral/Negative
5. 收入 (revenue):
6. 净利润 (net_income):
7. 现金及等价物 (cash_and_equivalents):
8. 总资产 (total_assets):
9. 总负债 (total_liabilities):
10. 股东权益 (shareholders_equity):
11. 自由现金流 (free_cash_flow):

返回有效的JSON格式，缺失的字段返回null。
"""
        return prompt

    def _call_spark_api(self, prompt: str) -> ExtractedIndicators:
        """调用Spark API（需要API配置）"""
        # 这里需要实现实际的API调用
        # 暂时返回mock结果
        logger.warning("Spark API call not fully implemented, using mock results")
        mock = MockExtractor()
        return mock.extract(prompt)


class OpenAIExtractor:
    """OpenAI GPT提取器"""

    def __init__(self):
        """初始化OpenAI提取器"""
        try:
            import openai
            self.available = True
        except ImportError:
            logger.warning("openai package not installed, using mock extractor")
            self.available = False
            self.mock_extractor = MockExtractor()

    def extract(
        self,
        text: str,
        company_name: Optional[str] = None
    ) -> ExtractedIndicators:
        """使用OpenAI API提取指标"""

        if not self.available:
            logger.warning("Using mock extractor as fallback")
            return self.mock_extractor.extract(text, company_name)

        try:
            # 构建提示词
            prompt = self._build_prompt(text, company_name)

            # 调用OpenAI API（需要配置API密钥）
            indicators = self._call_openai_api(prompt)
            return indicators

        except Exception as e:
            logger.error(f"OpenAI extraction failed: {str(e)}, using mock extractor")
            return self.mock_extractor.extract(text, company_name)

    def _build_prompt(self, text: str, company_name: Optional[str]) -> str:
        """构建提示词"""
        return f"""
Extract key financial indicators from the following report and return as JSON:

{text[:2000]}

Extract:
- audit_opinion (Unqualified/Qualified/Adverse/Disclaimer)
- industry_category
- negative_news_count and negative_news_items
- tone_factor (Positive/Neutral/Negative)
- revenue, net_income, cash_and_equivalents
- total_assets, total_liabilities, shareholders_equity
- free_cash_flow

Return valid JSON with null for missing values.
"""

    def _call_openai_api(self, prompt: str) -> ExtractedIndicators:
        """调用OpenAI API（需要配置）"""
        logger.warning("OpenAI API call not fully implemented, using mock results")
        mock = MockExtractor()
        return mock.extract(prompt)


# 便捷函数
def extract_key_indicators(
    financial_report_text: str,
    company_name: Optional[str] = None,
    backend: ExtractorBackend = ExtractorBackend.MOCK
) -> ExtractedIndicators:
    """
    快速提取关键指标

    Args:
        financial_report_text: 财务报告文本
        company_name: 公司名称
        backend: LLM后端

    Returns:
        提取的指标
    """
    extractor = KeyIndicatorExtractor(backend=backend)
    return extractor.extract_from_text(financial_report_text, company_name)


def extract_from_dict(
    financial_data: Dict[str, Any]
) -> ExtractedIndicators:
    """
    从字典中提取关键指标

    Args:
        financial_data: 财务数据字典

    Returns:
        提取的指标
    """
    extractor = KeyIndicatorExtractor()
    return extractor.extract_from_structured_data(financial_data)
