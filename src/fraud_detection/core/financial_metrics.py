"""
Financial Metrics Calculator
计算财务指标和各种评分
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FinancialRatios:
    """财务比率数据类"""
    roa_current: float
    roa_previous: float
    cfo_current: float
    leverage_current: float
    leverage_previous: float
    current_ratio_current: float
    current_ratio_previous: float
    shares_current: float
    shares_previous: float
    gross_margin_current: float
    gross_margin_previous: float
    asset_turnover_current: float
    asset_turnover_previous: float


class FinancialMetricsCalculator:
    """财务指标计算器"""

    def calculate_piotroski_fscore(self, ratios: Dict[str, float]) -> Dict[str, Any]:
        """
        计算Piotroski F-Score (0-9)
        衡量公司财务质量和盈利能力
        """
        score = 0
        details = {}

        # 1. ROA为正 +1
        if ratios.get('roa_current', 0) > 0:
            score += 1
            details['roa_positive'] = True
        else:
            details['roa_positive'] = False

        # 2. 运营现金流为正 +1
        if ratios.get('cfo_current', 0) > 0:
            score += 1
            details['cfo_positive'] = True
        else:
            details['cfo_positive'] = False

        # 3. ROA改善 +1
        if ratios.get('roa_current', 0) > ratios.get('roa_previous', 0):
            score += 1
            details['roa_improved'] = True
        else:
            details['roa_improved'] = False

        # 4. CFO > ROA +1
        if ratios.get('cfo_current', 0) > ratios.get('roa_current', 0):
            score += 1
            details['cfo_exceeds_roa'] = True
        else:
            details['cfo_exceeds_roa'] = False

        # 5. 杠杆降低 +1
        if ratios.get('leverage_current', 0) < ratios.get('leverage_previous', 0):
            score += 1
            details['leverage_decreased'] = True
        else:
            details['leverage_decreased'] = False

        # 6. 流动性改善 +1
        if ratios.get('current_ratio_current', 0) > ratios.get('current_ratio_previous', 0):
            score += 1
            details['liquidity_improved'] = True
        else:
            details['liquidity_improved'] = False

        # 7. 股份未增加 +1
        if ratios.get('shares_current', 0) <= ratios.get('shares_previous', 0):
            score += 1
            details['no_share_issuance'] = True
        else:
            details['no_share_issuance'] = False

        # 8. 毛利率改善 +1
        if ratios.get('gross_margin_current', 0) > ratios.get('gross_margin_previous', 0):
            score += 1
            details['gross_margin_improved'] = True
        else:
            details['gross_margin_improved'] = False

        # 9. 资产周转率改善 +1
        if ratios.get('asset_turnover_current', 0) > ratios.get('asset_turnover_previous', 0):
            score += 1
            details['asset_turnover_improved'] = True
        else:
            details['asset_turnover_improved'] = False

        return {
            'score': score,
            'max_score': 9,
            'percentage': round(score / 9 * 100, 2),
            'details': details
        }

    def calculate_fraud_fscore(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        计算欺诈F-Score (0-8+)
        检测财务操纵和异常的风险因子
        """
        score = 0
        risk_factors = {}

        # 1. RSST应计 > 0.1 +1
        rsst_accruals = metrics.get('rsst_accruals', 0)
        if rsst_accruals > 0.1:
            score += 1
            risk_factors['high_accruals'] = {
                'value': rsst_accruals,
                'threshold': 0.1,
                'flagged': True
            }
        else:
            risk_factors['high_accruals'] = {
                'value': rsst_accruals,
                'threshold': 0.1,
                'flagged': False
            }

        # 2. 应收账款增长 > 10% +1
        receivables_growth = metrics.get('receivables_growth', 0)
        if receivables_growth > 0.1:
            score += 1
            risk_factors['receivables_growth'] = {
                'value': receivables_growth,
                'threshold': 0.1,
                'flagged': True
            }
        else:
            risk_factors['receivables_growth'] = {
                'value': receivables_growth,
                'threshold': 0.1,
                'flagged': False
            }

        # 3. 库存增长 > 10% +1
        inventory_growth = metrics.get('inventory_growth', 0)
        if inventory_growth > 0.1:
            score += 1
            risk_factors['inventory_growth'] = {
                'value': inventory_growth,
                'threshold': 0.1,
                'flagged': True
            }
        else:
            risk_factors['inventory_growth'] = {
                'value': inventory_growth,
                'threshold': 0.1,
                'flagged': False
            }

        # 4. 软资产比率 > 0.5 +1
        soft_assets_ratio = metrics.get('soft_assets_ratio', 0)
        if soft_assets_ratio > 0.5:
            score += 1
            risk_factors['high_soft_assets'] = {
                'value': soft_assets_ratio,
                'threshold': 0.5,
                'flagged': True
            }
        else:
            risk_factors['high_soft_assets'] = {
                'value': soft_assets_ratio,
                'threshold': 0.5,
                'flagged': False
            }

        # 5. 销售和现金流差异增加 > 10% +1
        cash_sales_divergence = metrics.get('cash_sales_divergence', 0)
        if cash_sales_divergence > 0.1:
            score += 1
            risk_factors['cash_sales_divergence'] = {
                'value': cash_sales_divergence,
                'threshold': 0.1,
                'flagged': True
            }
        else:
            risk_factors['cash_sales_divergence'] = {
                'value': cash_sales_divergence,
                'threshold': 0.1,
                'flagged': False
            }

        # 6. ROA恶化 +1
        roa_deterioration = metrics.get('roa_deterioration', 0)
        if roa_deterioration < 0:
            score += 1
            risk_factors['roa_deterioration'] = {
                'value': roa_deterioration,
                'flagged': True
            }
        else:
            risk_factors['roa_deterioration'] = {
                'value': roa_deterioration,
                'flagged': False
            }

        # 7. 融资活动 > 0 +1
        refinancing_activity = metrics.get('refinancing_activity', 0)
        if refinancing_activity > 0:
            score += 1
            risk_factors['refinancing_activity'] = {
                'value': refinancing_activity,
                'flagged': True
            }
        else:
            risk_factors['refinancing_activity'] = {
                'value': refinancing_activity,
                'flagged': False
            }

        # 8. 员工变化异常 > 20% +1
        employee_change = metrics.get('abnormal_employee_change', 0)
        if abs(employee_change) > 0.2:
            score += 1
            risk_factors['abnormal_employee_change'] = {
                'value': employee_change,
                'threshold': 0.2,
                'flagged': True
            }
        else:
            risk_factors['abnormal_employee_change'] = {
                'value': employee_change,
                'threshold': 0.2,
                'flagged': False
            }

        # 9. 运营租赁增长 > 10% +1
        lease_growth = metrics.get('operating_lease_growth', 0)
        if lease_growth > 0.1:
            score += 1
            risk_factors['operating_lease_growth'] = {
                'value': lease_growth,
                'threshold': 0.1,
                'flagged': True
            }
        else:
            risk_factors['operating_lease_growth'] = {
                'value': lease_growth,
                'threshold': 0.1,
                'flagged': False
            }

        return {
            'score': score,
            'risk_factors': risk_factors,
            'flagged_count': sum(1 for f in risk_factors.values() if f.get('flagged'))
        }

    def calculate_sentiment_score(self, text: str) -> Dict[str, float]:
        """
        计算文本情感评分
        基于关键词检测
        """
        negative_keywords = [
            'risk', 'fraud', 'liability', 'default', 'delinquent',
            'lawsuit', 'investigation', 'violation', 'negative', '风险',
            '欺诈', '诉讼', '违规', '调查'
        ]
        positive_keywords = [
            'clean', 'no issue', 'audit clean', 'clear', 'positive',
            '清洁', '无问题', '审计清洁', '积极'
        ]

        score = 0.0
        text_lower = text.lower()

        for keyword in negative_keywords:
            score += text_lower.count(keyword.lower()) * 0.2

        for keyword in positive_keywords:
            score -= text_lower.count(keyword.lower()) * 0.1

        return {
            'sentiment_score': max(0.0, min(score, 1.0)),
            'negative_keyword_count': sum(
                text_lower.count(kw.lower()) for kw in negative_keywords
            ),
            'positive_keyword_count': sum(
                text_lower.count(kw.lower()) for kw in positive_keywords
            )
        }

    def calculate_cash_cycle_metrics(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        计算现金周期相关指标
        """
        receivable_days = metrics.get('receivable_days', 0)
        inventory_days = metrics.get('inventory_days', 0)
        payable_days = metrics.get('payable_days', 0)

        cash_cycle = receivable_days + inventory_days - payable_days

        return {
            'cash_cycle': cash_cycle,
            'receivable_days': receivable_days,
            'inventory_days': inventory_days,
            'payable_days': payable_days,
            'receivables_turnover': 365 / max(receivable_days, 1),
            'inventory_turnover': 365 / max(inventory_days, 1),
            'payables_turnover': 365 / max(payable_days, 1)
        }

    def calculate_liquidity_metrics(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        计算流动性指标
        """
        current_assets = metrics.get('current_assets', 0)
        current_liabilities = metrics.get('current_liabilities', 0)
        quick_assets = current_assets - metrics.get('inventory', 0)

        current_ratio = current_assets / max(current_liabilities, 0.01)
        quick_ratio = quick_assets / max(current_liabilities, 0.01)
        working_capital = current_assets - current_liabilities

        return {
            'current_ratio': current_ratio,
            'quick_ratio': quick_ratio,
            'working_capital': working_capital,
            'cash_ratio': metrics.get('cash', 0) / max(current_liabilities, 0.01)
        }

    def calculate_solvency_metrics(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        计算偿债能力指标
        """
        total_debt = metrics.get('total_debt', 0)
        total_assets = metrics.get('total_assets', 0)
        shareholders_equity = metrics.get('shareholders_equity', 0)
        ebit = metrics.get('ebit', 0)
        interest_expense = metrics.get('interest_expense', 0.01)

        return {
            'debt_ratio': total_debt / max(total_assets, 0.01),
            'debt_to_equity': total_debt / max(shareholders_equity, 0.01),
            'equity_ratio': shareholders_equity / max(total_assets, 0.01),
            'interest_coverage': ebit / max(interest_expense, 0.01),
            'debt_service_coverage': metrics.get('operating_cash_flow', 0) / max(
                total_debt * 0.1, 0.01
            )
        }

    def calculate_profitability_metrics(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        计算盈利能力指标
        """
        revenue = metrics.get('revenue', 0)
        net_income = metrics.get('net_income', 0)
        gross_profit = metrics.get('gross_profit', 0)
        total_assets = metrics.get('total_assets', 0)
        shareholders_equity = metrics.get('shareholders_equity', 0)

        return {
            'net_margin': net_income / max(revenue, 0.01),
            'gross_margin': gross_profit / max(revenue, 0.01),
            'roa': net_income / max(total_assets, 0.01),
            'roe': net_income / max(shareholders_equity, 0.01),
            'operating_margin': metrics.get('operating_income', 0) / max(revenue, 0.01),
            'ebitda_margin': metrics.get('ebitda', 0) / max(revenue, 0.01)
        }

    def calculate_efficiency_metrics(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        计算运营效率指标
        """
        revenue = metrics.get('revenue', 0)
        total_assets = metrics.get('total_assets', 0)
        inventory = metrics.get('inventory', 0)
        accounts_receivable = metrics.get('accounts_receivable', 0)

        return {
            'asset_turnover': revenue / max(total_assets, 0.01),
            'inventory_turnover': metrics.get('cogs', 0) / max(inventory, 0.01),
            'receivables_turnover': revenue / max(accounts_receivable, 0.01),
            'days_inventory': 365 / max(
                metrics.get('cogs', 0) / max(inventory, 0.01), 0.01
            ),
            'days_sales_outstanding': 365 / max(
                revenue / max(accounts_receivable, 0.01), 0.01
            )
        }

    def calculate_growth_metrics(
        self, current: Dict[str, float], previous: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算增长指标
        """
        def safe_growth(curr, prev):
            if prev == 0:
                return 1.0 if curr > 0 else -1.0
            return (curr - prev) / abs(prev)

        return {
            'revenue_growth': safe_growth(
                current.get('revenue', 0), previous.get('revenue', 0)
            ),
            'net_income_growth': safe_growth(
                current.get('net_income', 0), previous.get('net_income', 0)
            ),
            'asset_growth': safe_growth(
                current.get('total_assets', 0), previous.get('total_assets', 0)
            ),
            'equity_growth': safe_growth(
                current.get('shareholders_equity', 0),
                previous.get('shareholders_equity', 0)
            ),
            'gross_profit_growth': safe_growth(
                current.get('gross_profit', 0), previous.get('gross_profit', 0)
            )
        }
