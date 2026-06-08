"""
Data Fetcher Module - 从真实数据源获取财务数据
数据获取方式：SEC EDGAR API + NEWSAPI
"""

import logging
import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class DataFetcher:
    """从多个真实数据源获取公司财务数据"""

    def __init__(self, newsapi_key: str = None):
        """
        初始化数据获取器

        Args:
            newsapi_key: NewsAPI密钥
        """
        self.newsapi_key = newsapi_key
        self.sec_edgar_url = "https://www.sec.gov/cgi-bin"
        self.newsapi_base_url = "https://newsapi.org/v2"

    def fetch_company_financials(self, ticker: str, cik: str = None) -> Dict[str, Any]:
        """
        从SEC EDGAR数据库获取公司财务数据

        三大部分数据：
        1. 收入报表 (Income Statement)
        2. 资产负债表 (Balance Sheet)
        3. 现金流量表 (Cash Flow Statement)

        Args:
            ticker: 股票代码 (e.g., 'AAPL')
            cik: CIK号码 (如果已知)

        Returns:
            包含财务数据的字典
        """
        logger.info(f"Fetching financial data for {ticker} from SEC EDGAR")

        result = {
            'ticker': ticker,
            'fetch_timestamp': datetime.now().isoformat(),
            'source': 'SEC EDGAR',
            'data': {
                'income_statement': {},
                'balance_sheet': {},
                'cash_flow_statement': {},
                'key_metrics': {}
            }
        }

        try:
            # 获取CIK号码
            if not cik:
                cik = self._get_cik_from_ticker(ticker)
                if not cik:
                    logger.error(f"Could not find CIK for ticker {ticker}")
                    result['error'] = f"CIK not found for {ticker}"
                    return result

            # 从SEC EDGAR获取10-K或10-Q文件
            filings = self._fetch_sec_filings(cik, ticker)
            if filings:
                result['data'] = self._parse_sec_filings(filings)
                logger.info(f"Retrieved financial data for {ticker}")
            else:
                logger.warning(f"No filings found for {ticker}")
                result['error'] = "No SEC filings found"

        except Exception as e:
            logger.error(f"Error fetching financial data: {str(e)}")
            result['error'] = str(e)

        return result

    def _get_cik_from_ticker(self, ticker: str) -> Optional[str]:
        """
        从SEC EDGAR获取公司的CIK号码

        Args:
            ticker: 股票代码

        Returns:
            CIK号码或None
        """
        try:
            # 使用SEC的公司搜索API
            url = f"{self.sec_edgar_url}/browse-edgar"
            params = {
                'action': 'getcompany',
                'company': ticker,
                'type': '10-K',
                'dateb': '',
                'owner': 'exclude',
                'count': 40,
                'output': 'json'
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'cik_lookup' in data and len(data['cik_lookup']) > 0:
                    cik = str(data['cik_lookup'][0]['cik_number']).zfill(10)
                    logger.debug(f"Found CIK {cik} for ticker {ticker}")
                    return cik

        except Exception as e:
            logger.warning(f"Error getting CIK for {ticker}: {e}")

        return None

    def _fetch_sec_filings(self, cik: str, ticker: str) -> Optional[Dict[str, Any]]:
        """
        从SEC EDGAR获取最近的10-K或10-Q文件

        Args:
            cik: CIK号码
            ticker: 股票代码

        Returns:
            最近的filing数据或None
        """
        try:
            # 使用SEC的JSON API获取company facts
            url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"Retrieved SEC data for CIK {cik}")
                return data
            else:
                logger.warning(f"SEC API returned status {response.status_code}")

        except Exception as e:
            logger.error(f"Error fetching SEC filings: {e}")

        return None

    def _parse_sec_filings(self, sec_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析SEC EDGAR数据并提取财务报表

        Args:
            sec_data: 来自SEC API的数据

        Returns:
            结构化的财务数据
        """
        data = {
            'income_statement': {},
            'balance_sheet': {},
            'cash_flow_statement': {},
            'key_metrics': {}
        }

        try:
            if 'facts' not in sec_data or 'us-gaap' not in sec_data['facts']:
                return data

            us_gaap = sec_data['facts']['us-gaap']

            # 提取收入报表指标
            income_statement_keys = [
                'Revenues', 'CostOfRevenue', 'GrossProfit',
                'OperatingExpenses', 'OperatingIncomeLoss',
                'NetIncomeLoss'
            ]

            for key in income_statement_keys:
                if key in us_gaap:
                    values = us_gaap[key]['units'].get('USD', [])
                    if values:
                        # 获取最新的值
                        latest = max(values, key=lambda x: x.get('end', ''))
                        data['income_statement'][key] = latest.get('val')

            # 提取资产负债表指标
            balance_sheet_keys = [
                'Assets', 'CurrentAssets', 'AssetsCurrent',
                'Liabilities', 'CurrentLiabilities',
                'LiabilitiesCurrent', 'StockholdersEquity',
                'CommonStockSharesOutstanding'
            ]

            for key in balance_sheet_keys:
                if key in us_gaap:
                    values = us_gaap[key]['units'].get('USD', [])
                    if values:
                        latest = max(values, key=lambda x: x.get('end', ''))
                        data['balance_sheet'][key] = latest.get('val')

            # 提取现金流指标
            cash_flow_keys = [
                'NetCashProvidedByOperatingActivities',
                'NetCashUsedInInvestingActivities',
                'NetCashProvidedByFinancingActivities',
                'CashAtEndOfPeriod'
            ]

            for key in cash_flow_keys:
                if key in us_gaap:
                    values = us_gaap[key]['units'].get('USD', [])
                    if values:
                        latest = max(values, key=lambda x: x.get('end', ''))
                        data['cash_flow_statement'][key] = latest.get('val')

            logger.debug("Successfully parsed SEC EDGAR data")

        except Exception as e:
            logger.error(f"Error parsing SEC data: {e}")

        return data

    def fetch_company_news(self, ticker: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        获取公司相关新闻（使用NEWSAPI）

        Args:
            ticker: 股票代码
            days: 回溯天数

        Returns:
            新闻列表
        """
        logger.info(f"Fetching news for {ticker}")

        news_list = []

        if not self.newsapi_key:
            logger.warning("NewsAPI key not configured")
            return news_list

        try:
            # 计算日期范围
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # 构建查询
            query = f"{ticker} company"
            params = {
                'q': query,
                'apiKey': self.newsapi_key,
                'sortBy': 'publishedAt',
                'language': 'en',
                'from': start_date.isoformat(),
                'to': end_date.isoformat()
            }

            # 调用NewsAPI
            response = requests.get(f"{self.newsapi_base_url}/everything", params=params)

            if response.status_code == 200:
                data = response.json()
                if 'articles' in data:
                    news_list = [
                        {
                            'title': article.get('title'),
                            'description': article.get('description'),
                            'source': article.get('source', {}).get('name'),
                            'published_at': article.get('publishedAt'),
                            'url': article.get('url'),
                            'sentiment': self._analyze_news_sentiment(article.get('description', ''))
                        }
                        for article in data['articles']
                    ]
                    logger.info(f"Retrieved {len(news_list)} news articles for {ticker}")
            else:
                logger.warning(f"NewsAPI returned status {response.status_code}")

        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")

        return news_list

    def fetch_sec_filings_metadata(self, ticker: str, cik: str = None, filing_type: str = '10-K') -> List[Dict[str, Any]]:
        """
        获取SEC filing元数据

        Args:
            ticker: 股票代码
            cik: CIK号码
            filing_type: filing类型 (10-K, 10-Q, 8-K等)

        Returns:
            SEC filing列表
        """
        logger.info(f"Fetching SEC {filing_type} filings for {ticker}")

        filings = []

        try:
            # 获取CIK号码
            if not cik:
                cik = self._get_cik_from_ticker(ticker)
                if not cik:
                    return filings

            # 使用SEC的公司浏览API获取filing信息
            url = f"{self.sec_edgar_url}/browse-edgar"
            params = {
                'action': 'getcompany',
                'CIK': cik,
                'type': filing_type,
                'dateb': '',
                'owner': 'exclude',
                'count': 10,
                'output': 'json'
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'filings' in data and 'files' in data['filings']:
                    filings = [
                        {
                            'accession_number': f.get('accession_number'),
                            'filing_date': f.get('filing_date'),
                            'report_date': f.get('report_date'),
                            'filing_type': f.get('form'),
                            'url': f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={filing_type}&dateb=&owner=exclude&count=100"
                        }
                        for f in data['filings']['files'][:10]  # 获取最近10个
                    ]
                    logger.info(f"Retrieved {len(filings)} {filing_type} filings")

        except Exception as e:
            logger.error(f"Error fetching SEC filings metadata: {str(e)}")

        return filings

    def _analyze_news_sentiment(self, text: str) -> str:
        """
        简单的新闻情感分析

        Args:
            text: 新闻文本

        Returns:
            情感标签 (positive/neutral/negative)
        """
        if not text:
            return 'neutral'

        negative_words = ['decline', 'loss', 'lawsuit', 'fraud', 'risk', 'warning', 'investigation']
        positive_words = ['gain', 'profit', 'success', 'growth', 'beat', 'strong']

        text_lower = text.lower()

        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)

        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        else:
            return 'neutral'

    def compile_financial_report(
        self,
        ticker: str,
        cik: str = None,
        include_news: bool = True,
        include_sec_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        编译完整的财务报告（三大部分）

        包含：
        1. 财务数据 (SEC EDGAR)
        2. 新闻和市场舆论 (NewsAPI)
        3. SEC Filing元数据

        Args:
            ticker: 股票代码
            cik: CIK号码
            include_news: 是否包含新闻
            include_sec_metadata: 是否包含SEC metadata

        Returns:
            完整的财务报告
        """
        logger.info(f"Compiling financial report for {ticker}")

        report = {
            'ticker': ticker,
            'compiled_at': datetime.now().isoformat(),
            'source': 'SEC EDGAR + NewsAPI',
            'components': {}
        }

        # 第一部分：财务数据（来自SEC EDGAR）
        report['components']['financial_data'] = self.fetch_company_financials(ticker, cik)

        # 第二部分：新闻和舆论（来自NewsAPI）
        if include_news:
            report['components']['news'] = self.fetch_company_news(ticker)

        # 第三部分：SEC Filing元数据
        if include_sec_metadata:
            report['components']['sec_filings'] = self.fetch_sec_filings_metadata(ticker, cik)

        return report


# 便捷函数
def fetch_financial_report(
    ticker: str,
    newsapi_key: str = None
) -> Dict[str, Any]:
    """
    快速获取完整的财务报告（来自SEC EDGAR和NewsAPI）

    Args:
        ticker: 股票代码
        newsapi_key: NewsAPI密钥

    Returns:
        完整的财务报告
    """
    fetcher = DataFetcher(newsapi_key=newsapi_key)
    return fetcher.compile_financial_report(ticker)


    def fetch_company_financials(self, ticker: str) -> Dict[str, Any]:
        """
        使用OpenBB SDK或FMP API获取公司财务数据

        三大部分数据：
        1. 收入报表 (Income Statement)
        2. 资产负债表 (Balance Sheet)
        3. 现金流量表 (Cash Flow Statement)

        Args:
            ticker: 股票代码 (e.g., 'AAPL')

        Returns:
            包含财务数据的字典
        """
        logger.info(f"Fetching financial data for {ticker}")

        result = {
            'ticker': ticker,
            'fetch_timestamp': datetime.now().isoformat(),
            'data': {
                'income_statement': {},
                'balance_sheet': {},
                'cash_flow_statement': {},
                'key_metrics': {}
            }
        }

        try:
            # 尝试使用OpenBB SDK
            try:
                from openbb import obb
                logger.info("Using OpenBB SDK for data fetching")
                result['data'] = self._fetch_with_openbb(obb, ticker)
                result['source'] = 'OpenBB SDK'
            except ImportError:
                logger.warning("OpenBB not installed, falling back to FMP API")
                result['data'] = self._fetch_with_fmp_api(ticker)
                result['source'] = 'FMP API'

        except Exception as e:
            logger.error(f"Error fetching financial data: {str(e)}")
            result['error'] = str(e)

        return result

    def _fetch_with_openbb(self, obb, ticker: str) -> Dict[str, Any]:
        """使用OpenBB SDK获取财务数据"""
        try:
            data = {
                'income_statement': {},
                'balance_sheet': {},
                'cash_flow_statement': {},
                'key_metrics': {}
            }

            # 获取收入报表
            try:
                income_stmt = obb.stocks.fundamentals.income(ticker)
                if income_stmt is not None:
                    data['income_statement'] = self._parse_financial_data(income_stmt)
                    logger.debug(f"Retrieved income statement for {ticker}")
            except Exception as e:
                logger.warning(f"Failed to fetch income statement: {e}")

            # 获取资产负债表
            try:
                balance_sheet = obb.stocks.fundamentals.balance(ticker)
                if balance_sheet is not None:
                    data['balance_sheet'] = self._parse_financial_data(balance_sheet)
                    logger.debug(f"Retrieved balance sheet for {ticker}")
            except Exception as e:
                logger.warning(f"Failed to fetch balance sheet: {e}")

            # 获取现金流量表
            try:
                cash_flow = obb.stocks.fundamentals.cash(ticker)
                if cash_flow is not None:
                    data['cash_flow_statement'] = self._parse_financial_data(cash_flow)
                    logger.debug(f"Retrieved cash flow statement for {ticker}")
            except Exception as e:
                logger.warning(f"Failed to fetch cash flow: {e}")

            # 获取关键指标
            try:
                metrics = obb.stocks.fundamentals.metrics(ticker)
                if metrics is not None:
                    data['key_metrics'] = self._parse_financial_data(metrics)
                    logger.debug(f"Retrieved key metrics for {ticker}")
            except Exception as e:
                logger.warning(f"Failed to fetch metrics: {e}")

            return data

        except Exception as e:
            logger.error(f"OpenBB fetch error: {str(e)}")
            raise

    def _fetch_with_fmp_api(self, ticker: str) -> Dict[str, Any]:
        """使用FMP API获取财务数据（备用方案）"""
        data = {
            'income_statement': {},
            'balance_sheet': {},
            'cash_flow_statement': {},
            'key_metrics': {}
        }

        if not self.fmp_api_key:
            logger.warning("FMP API key not configured")
            return data

        try:
            # 获取收入报表
            income_url = f"{self.fmp_base_url}/income-statement/{ticker}?apikey={self.fmp_api_key}"
            resp = requests.get(income_url)
            if resp.status_code == 200:
                data['income_statement'] = resp.json()

            # 获取资产负债表
            balance_url = f"{self.fmp_base_url}/balance-sheet-statement/{ticker}?apikey={self.fmp_api_key}"
            resp = requests.get(balance_url)
            if resp.status_code == 200:
                data['balance_sheet'] = resp.json()

            # 获取现金流量表
            cashflow_url = f"{self.fmp_base_url}/cash-flow-statement/{ticker}?apikey={self.fmp_api_key}"
            resp = requests.get(cashflow_url)
            if resp.status_code == 200:
                data['cash_flow_statement'] = resp.json()

            # 获取关键指标
            metrics_url = f"{self.fmp_base_url}/ratios/{ticker}?apikey={self.fmp_api_key}"
            resp = requests.get(metrics_url)
            if resp.status_code == 200:
                data['key_metrics'] = resp.json()

            return data

        except Exception as e:
            logger.error(f"FMP API fetch error: {str(e)}")
            return data

    def fetch_company_news(self, ticker: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        获取公司相关新闻（使用NEWSAPI）

        Args:
            ticker: 股票代码
            days: 回溯天数

        Returns:
            新闻列表
        """
        logger.info(f"Fetching news for {ticker}")

        news_list = []

        if not self.newsapi_key:
            logger.warning("NewsAPI key not configured")
            return news_list

        try:
            # 计算日期范围
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # 构建查询
            query = f"{ticker} company"
            params = {
                'q': query,
                'apiKey': self.newsapi_key,
                'sortBy': 'publishedAt',
                'language': 'en',
                'from': start_date.isoformat(),
                'to': end_date.isoformat()
            }

            # 调用NewsAPI
            response = requests.get(f"{self.newsapi_base_url}/everything", params=params)

            if response.status_code == 200:
                data = response.json()
                if 'articles' in data:
                    news_list = [
                        {
                            'title': article.get('title'),
                            'description': article.get('description'),
                            'source': article.get('source', {}).get('name'),
                            'published_at': article.get('publishedAt'),
                            'url': article.get('url'),
                            'sentiment': self._analyze_news_sentiment(article.get('description', ''))
                        }
                        for article in data['articles']
                    ]
                    logger.info(f"Retrieved {len(news_list)} news articles for {ticker}")
            else:
                logger.warning(f"NewsAPI returned status {response.status_code}")

        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")

        return news_list

    def fetch_sec_filings(self, ticker: str, filing_type: str = '10-K') -> List[Dict[str, Any]]:
        """
        获取SEC filing文件信息

        Args:
            ticker: 股票代码
            filing_type: filing类型 (10-K, 10-Q, 8-K等)

        Returns:
            SEC filing列表
        """
        logger.info(f"Fetching SEC {filing_type} filings for {ticker}")

        filings = []

        try:
            # 使用FMP API或SEC EDGAR API
            if self.fmp_api_key:
                url = f"{self.fmp_base_url}/sec_filings/{ticker}?type={filing_type}&apikey={self.fmp_api_key}"
                response = requests.get(url)

                if response.status_code == 200:
                    filings = response.json()
                    logger.info(f"Retrieved {len(filings)} {filing_type} filings")

        except Exception as e:
            logger.error(f"Error fetching SEC filings: {str(e)}")

        return filings

    def _parse_financial_data(self, raw_data: Any) -> Dict[str, Any]:
        """
        解析原始财务数据

        Args:
            raw_data: 来自API的原始数据

        Returns:
            解析后的数据字典
        """
        try:
            if isinstance(raw_data, dict):
                return raw_data
            elif hasattr(raw_data, 'to_dict'):
                return raw_data.to_dict()
            elif hasattr(raw_data, 'model_dump'):
                return raw_data.model_dump()
            else:
                return str(raw_data)
        except Exception as e:
            logger.warning(f"Error parsing financial data: {e}")
            return {}

    def _analyze_news_sentiment(self, text: str) -> str:
        """
        简单的新闻情感分析

        Args:
            text: 新闻文本

        Returns:
            情感标签 (positive/neutral/negative)
        """
        if not text:
            return 'neutral'

        negative_words = ['decline', 'loss', 'lawsuit', 'fraud', 'risk', 'warning']
        positive_words = ['gain', 'profit', 'success', 'growth', 'beat']

        text_lower = text.lower()

        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)

        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        else:
            return 'neutral'

    def compile_financial_report(
        self,
        ticker: str,
        include_news: bool = True,
        include_sec_filings: bool = True
    ) -> Dict[str, Any]:
        """
        编译完整的财务报告（三大部分）

        包含：
        1. 财务数据 (OpenBB/FMP)
        2. 新闻和市场舆论 (NewsAPI)
        3. SEC Filings信息

        Args:
            ticker: 股票代码
            include_news: 是否包含新闻
            include_sec_filings: 是否包含SEC filings

        Returns:
            完整的财务报告
        """
        logger.info(f"Compiling financial report for {ticker}")

        report = {
            'ticker': ticker,
            'compiled_at': datetime.now().isoformat(),
            'components': {}
        }

        # 第一部分：财务数据
        report['components']['financial_data'] = self.fetch_company_financials(ticker)

        # 第二部分：新闻和舆论
        if include_news:
            report['components']['news'] = self.fetch_company_news(ticker)

        # 第三部分：SEC Filings
        if include_sec_filings:
            report['components']['sec_filings'] = self.fetch_sec_filings(ticker)

        return report


# 便捷函数
def fetch_financial_report(
    ticker: str,
    fmp_api_key: str = None,
    newsapi_key: str = None
) -> Dict[str, Any]:
    """
    快速获取完整的财务报告

    Args:
        ticker: 股票代码
        fmp_api_key: FMP API密钥
        newsapi_key: NewsAPI密钥

    Returns:
        完整的财务报告
    """
    fetcher = DataFetcher(fmp_api_key=fmp_api_key, newsapi_key=newsapi_key)
    return fetcher.compile_financial_report(ticker)
