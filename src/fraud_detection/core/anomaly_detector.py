"""
Anomaly Detection and Risk Scoring System
异常检测和风险评分系统
"""

import logging
from typing import Dict, Any, List, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """风险等级"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class AnomalyDetector:
    """异常检测器 - 识别财务异常"""

    def __init__(self):
        self.thresholds = {
            'cashflow': {
                'cash_cycle': {'warn': -90, 'critical': -180, 'weight_warn': 1, 'weight_critical': 2},
                'cfo_to_net_income': {'warn': 0.8, 'critical': 0.5, 'weight_warn': 0.5, 'weight_critical': 1},
                'inventory_days': {'warn': 60, 'critical': 90, 'weight_warn': 0.5, 'weight_critical': 1},
                'payable_days': {'warn': 90, 'critical': 180, 'weight_warn': 0.5, 'weight_critical': 1},
                'payables_turnover': {'warn': 1.5, 'critical': 1.0, 'weight_warn': 0.5, 'weight_critical': 1},
                'receivable_days': {'warn': 60, 'critical': 120, 'weight_warn': 0.5, 'weight_critical': 1},
            },
            'solvency': {
                'debt_ratio': {'warn': 0.6, 'critical': 0.8, 'weight_warn': 1, 'weight_critical': 2},
                'current_ratio': {'warn': 1.2, 'critical': 1.0, 'weight_warn': 0.5, 'weight_critical': 1},
                'quick_ratio': {'warn': 1.0, 'critical': 0.8, 'weight_warn': 0.5, 'weight_critical': 1},
            },
            'profitability': {
                'roa': {'warn': 0.08, 'critical': 0.05, 'weight_warn': 0.5, 'weight_critical': 1},
                'net_margin': {'warn': 0.15, 'critical': 0.10, 'weight_warn': 0.5, 'weight_critical': 1},
            },
            'growth': {
                'net_income_growth': {'warn': 0.0, 'critical': -0.1, 'weight_warn': 0.5, 'weight_critical': 1},
            }
        }

    def detect_anomalies(
        self,
        current_metrics: Dict[str, float],
        previous_metrics: Dict[str, float],
        fraud_score: int,
        piotroski_score: int
    ) -> Dict[str, Any]:
        """
        检测异常和识别风险因子

        Args:
            current_metrics: 当期财务指标
            previous_metrics: 上期财务指标
            fraud_score: 欺诈F-Score
            piotroski_score: Piotroski评分

        Returns:
            包含异常信息和风险因子的字典
        """
        risk_score = 0.0
        risk_factors = []

        # 检测现金流异常
        cashflow_anomalies = self._detect_cashflow_anomalies(current_metrics)
        risk_score += cashflow_anomalies['score']
        risk_factors.extend(cashflow_anomalies['factors'])

        # 检测偿债能力异常
        solvency_anomalies = self._detect_solvency_anomalies(current_metrics)
        risk_score += solvency_anomalies['score']
        risk_factors.extend(solvency_anomalies['factors'])

        # 检测盈利能力异常
        profitability_anomalies = self._detect_profitability_anomalies(
            current_metrics, previous_metrics
        )
        risk_score += profitability_anomalies['score']
        risk_factors.extend(profitability_anomalies['factors'])

        # 检测增长异常
        growth_anomalies = self._detect_growth_anomalies(
            current_metrics, previous_metrics
        )
        risk_score += growth_anomalies['score']
        risk_factors.extend(growth_anomalies['factors'])

        # 添加欺诈评分贡献
        fraud_contribution = self._calculate_fraud_contribution(fraud_score)
        risk_score += fraud_contribution['score']
        risk_factors.extend(fraud_contribution['factors'])

        # 添加Piotroski评分贡献
        piotroski_contribution = self._calculate_piotroski_contribution(piotroski_score)
        risk_score += piotroski_contribution['score']
        risk_factors.extend(piotroski_contribution['factors'])

        # 确定风险等级
        risk_level = self._determine_risk_level(risk_score)

        # 排序和筛选风险因子
        sorted_factors = sorted(
            risk_factors, key=lambda x: x['contribution'], reverse=True
        )
        top_5_factors = sorted_factors[:5]

        return {
            'risk_score': min(risk_score, 100),  # 限制在0-100
            'risk_level': risk_level,
            'total_factors': len(risk_factors),
            'top_5_factors': top_5_factors,
            'all_factors': sorted_factors,
            'score_components': {
                'cashflow': cashflow_anomalies['score'],
                'solvency': solvency_anomalies['score'],
                'profitability': profitability_anomalies['score'],
                'growth': growth_anomalies['score'],
                'fraud': fraud_contribution['score'],
                'piotroski': piotroski_contribution['score']
            }
        }

    def _detect_cashflow_anomalies(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """检测现金流异常"""
        score = 0.0
        factors = []
        thresholds = self.thresholds['cashflow']

        # 检查现金周期
        cash_cycle = metrics.get('cash_cycle', 0)
        if cash_cycle >= thresholds['cash_cycle']['critical']:
            score += thresholds['cash_cycle']['weight_critical']
            factors.append({
                'name': 'cash_cycle_critical',
                'description': f'现金周期过长 ({cash_cycle} 天)',
                'value': cash_cycle,
                'threshold': thresholds['cash_cycle']['critical'],
                'severity': 'critical',
                'contribution': thresholds['cash_cycle']['weight_critical']
            })
        elif cash_cycle >= thresholds['cash_cycle']['warn']:
            score += thresholds['cash_cycle']['weight_warn']
            factors.append({
                'name': 'cash_cycle_warning',
                'description': f'现金周期较长 ({cash_cycle} 天)',
                'value': cash_cycle,
                'threshold': thresholds['cash_cycle']['warn'],
                'severity': 'warning',
                'contribution': thresholds['cash_cycle']['weight_warn']
            })

        # 检查应收账款天数
        receivable_days = metrics.get('receivable_days', 0)
        if receivable_days >= thresholds['receivable_days']['critical']:
            score += thresholds['receivable_days']['weight_critical']
            factors.append({
                'name': 'high_receivable_days_critical',
                'description': f'应收账款周期过长 ({receivable_days} 天)',
                'value': receivable_days,
                'threshold': thresholds['receivable_days']['critical'],
                'severity': 'critical',
                'contribution': thresholds['receivable_days']['weight_critical']
            })
        elif receivable_days >= thresholds['receivable_days']['warn']:
            score += thresholds['receivable_days']['weight_warn']
            factors.append({
                'name': 'high_receivable_days_warning',
                'description': f'应收账款周期较长 ({receivable_days} 天)',
                'value': receivable_days,
                'threshold': thresholds['receivable_days']['warn'],
                'severity': 'warning',
                'contribution': thresholds['receivable_days']['weight_warn']
            })

        # 检查库存天数
        inventory_days = metrics.get('inventory_days', 0)
        if inventory_days >= thresholds['inventory_days']['critical']:
            score += thresholds['inventory_days']['weight_critical']
            factors.append({
                'name': 'high_inventory_days_critical',
                'description': f'库存周期过长 ({inventory_days} 天)',
                'value': inventory_days,
                'threshold': thresholds['inventory_days']['critical'],
                'severity': 'critical',
                'contribution': thresholds['inventory_days']['weight_critical']
            })
        elif inventory_days >= thresholds['inventory_days']['warn']:
            score += thresholds['inventory_days']['weight_warn']
            factors.append({
                'name': 'high_inventory_days_warning',
                'description': f'库存周期较长 ({inventory_days} 天)',
                'value': inventory_days,
                'threshold': thresholds['inventory_days']['warn'],
                'severity': 'warning',
                'contribution': thresholds['inventory_days']['weight_warn']
            })

        return {'score': score, 'factors': factors}

    def _detect_solvency_anomalies(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """检测偿债能力异常"""
        score = 0.0
        factors = []
        thresholds = self.thresholds['solvency']

        # 检查债务比率
        debt_ratio = metrics.get('debt_ratio', 0)
        if debt_ratio >= thresholds['debt_ratio']['critical']:
            score += thresholds['debt_ratio']['weight_critical']
            factors.append({
                'name': 'high_debt_ratio_critical',
                'description': f'债务比率过高 ({debt_ratio:.2%})',
                'value': debt_ratio,
                'threshold': thresholds['debt_ratio']['critical'],
                'severity': 'critical',
                'contribution': thresholds['debt_ratio']['weight_critical']
            })
        elif debt_ratio >= thresholds['debt_ratio']['warn']:
            score += thresholds['debt_ratio']['weight_warn']
            factors.append({
                'name': 'high_debt_ratio_warning',
                'description': f'债务比率较高 ({debt_ratio:.2%})',
                'value': debt_ratio,
                'threshold': thresholds['debt_ratio']['warn'],
                'severity': 'warning',
                'contribution': thresholds['debt_ratio']['weight_warn']
            })

        # 检查流动比率
        current_ratio = metrics.get('current_ratio', 0)
        if current_ratio <= thresholds['current_ratio']['critical']:
            score += thresholds['current_ratio']['weight_critical']
            factors.append({
                'name': 'low_current_ratio_critical',
                'description': f'流动比率过低 ({current_ratio:.2f})',
                'value': current_ratio,
                'threshold': thresholds['current_ratio']['critical'],
                'severity': 'critical',
                'contribution': thresholds['current_ratio']['weight_critical']
            })
        elif current_ratio <= thresholds['current_ratio']['warn']:
            score += thresholds['current_ratio']['weight_warn']
            factors.append({
                'name': 'low_current_ratio_warning',
                'description': f'流动比率较低 ({current_ratio:.2f})',
                'value': current_ratio,
                'threshold': thresholds['current_ratio']['warn'],
                'severity': 'warning',
                'contribution': thresholds['current_ratio']['weight_warn']
            })

        # 检查速动比率
        quick_ratio = metrics.get('quick_ratio', 0)
        if quick_ratio <= thresholds['quick_ratio']['critical']:
            score += thresholds['quick_ratio']['weight_critical']
            factors.append({
                'name': 'low_quick_ratio_critical',
                'description': f'速动比率过低 ({quick_ratio:.2f})',
                'value': quick_ratio,
                'threshold': thresholds['quick_ratio']['critical'],
                'severity': 'critical',
                'contribution': thresholds['quick_ratio']['weight_critical']
            })
        elif quick_ratio <= thresholds['quick_ratio']['warn']:
            score += thresholds['quick_ratio']['weight_warn']
            factors.append({
                'name': 'low_quick_ratio_warning',
                'description': f'速动比率较低 ({quick_ratio:.2f})',
                'value': quick_ratio,
                'threshold': thresholds['quick_ratio']['warn'],
                'severity': 'warning',
                'contribution': thresholds['quick_ratio']['weight_warn']
            })

        return {'score': score, 'factors': factors}

    def _detect_profitability_anomalies(
        self,
        current: Dict[str, float],
        previous: Dict[str, float]
    ) -> Dict[str, Any]:
        """检测盈利能力异常"""
        score = 0.0
        factors = []
        thresholds = self.thresholds['profitability']

        # 检查ROA
        roa = current.get('roa', 0)
        if roa <= thresholds['roa']['critical']:
            score += thresholds['roa']['weight_critical']
            factors.append({
                'name': 'low_roa_critical',
                'description': f'总资产收益率过低 ({roa:.2%})',
                'value': roa,
                'threshold': thresholds['roa']['critical'],
                'severity': 'critical',
                'contribution': thresholds['roa']['weight_critical']
            })
        elif roa <= thresholds['roa']['warn']:
            score += thresholds['roa']['weight_warn']
            factors.append({
                'name': 'low_roa_warning',
                'description': f'总资产收益率较低 ({roa:.2%})',
                'value': roa,
                'threshold': thresholds['roa']['warn'],
                'severity': 'warning',
                'contribution': thresholds['roa']['weight_warn']
            })

        # 检查净利率
        net_margin = current.get('net_margin', 0)
        if net_margin <= thresholds['net_margin']['critical']:
            score += thresholds['net_margin']['weight_critical']
            factors.append({
                'name': 'low_net_margin_critical',
                'description': f'净利率过低 ({net_margin:.2%})',
                'value': net_margin,
                'threshold': thresholds['net_margin']['critical'],
                'severity': 'critical',
                'contribution': thresholds['net_margin']['weight_critical']
            })
        elif net_margin <= thresholds['net_margin']['warn']:
            score += thresholds['net_margin']['weight_warn']
            factors.append({
                'name': 'low_net_margin_warning',
                'description': f'净利率较低 ({net_margin:.2%})',
                'value': net_margin,
                'threshold': thresholds['net_margin']['warn'],
                'severity': 'warning',
                'contribution': thresholds['net_margin']['weight_warn']
            })

        return {'score': score, 'factors': factors}

    def _detect_growth_anomalies(
        self,
        current: Dict[str, float],
        previous: Dict[str, float]
    ) -> Dict[str, Any]:
        """检测增长异常"""
        score = 0.0
        factors = []
        thresholds = self.thresholds['growth']

        # 计算净利润增长
        if previous.get('net_income', 0) != 0:
            growth = (current.get('net_income', 0) - previous.get('net_income', 0)) / abs(
                previous.get('net_income', 0)
            )
        else:
            growth = 1.0 if current.get('net_income', 0) > 0 else -1.0

        if growth <= thresholds['net_income_growth']['critical']:
            score += thresholds['net_income_growth']['weight_critical']
            factors.append({
                'name': 'negative_growth_critical',
                'description': f'净利润严重下滑 ({growth:.2%})',
                'value': growth,
                'threshold': thresholds['net_income_growth']['critical'],
                'severity': 'critical',
                'contribution': thresholds['net_income_growth']['weight_critical']
            })
        elif growth <= thresholds['net_income_growth']['warn']:
            score += thresholds['net_income_growth']['weight_warn']
            factors.append({
                'name': 'negative_growth_warning',
                'description': f'净利润下滑 ({growth:.2%})',
                'value': growth,
                'threshold': thresholds['net_income_growth']['warn'],
                'severity': 'warning',
                'contribution': thresholds['net_income_growth']['weight_warn']
            })

        return {'score': score, 'factors': factors}

    def _calculate_fraud_contribution(self, fraud_score: int) -> Dict[str, Any]:
        """计算欺诈分数的贡献"""
        score = 0.0
        factors = []

        if fraud_score >= 5:
            score = 3
            factors.append({
                'name': 'high_fraud_risk',
                'description': f'欺诈风险分数过高 ({fraud_score}/9)',
                'value': fraud_score,
                'threshold': 5,
                'severity': 'critical',
                'contribution': score
            })
        elif fraud_score >= 3:
            score = 1.5
            factors.append({
                'name': 'medium_fraud_risk',
                'description': f'欺诈风险分数中等 ({fraud_score}/9)',
                'value': fraud_score,
                'threshold': 3,
                'severity': 'warning',
                'contribution': score
            })

        return {'score': score, 'factors': factors}

    def _calculate_piotroski_contribution(self, piotroski_score: int) -> Dict[str, Any]:
        """计算Piotroski分数的贡献"""
        score = 0.0
        factors = []

        if piotroski_score <= 4:
            score = 2
            factors.append({
                'name': 'low_piotroski_score',
                'description': f'Piotroski评分过低 ({piotroski_score}/9)',
                'value': piotroski_score,
                'threshold': 4,
                'severity': 'critical',
                'contribution': score
            })
        elif piotroski_score <= 6:
            score = 1
            factors.append({
                'name': 'medium_piotroski_score',
                'description': f'Piotroski评分中等 ({piotroski_score}/9)',
                'value': piotroski_score,
                'threshold': 6,
                'severity': 'warning',
                'contribution': score
            })

        return {'score': score, 'factors': factors}

    def _determine_risk_level(self, risk_score: float) -> str:
        """确定风险等级"""
        if risk_score >= 15:
            return RiskLevel.HIGH.value
        elif risk_score >= 8:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.LOW.value
