"""
Financial Fraud Detection Analysis Pipeline
财务欺诈检测分析管道
"""

import logging
from typing import Dict, Any, Optional
from fraud_detection.core.financial_metrics import FinancialMetricsCalculator
from fraud_detection.core.anomaly_detector import AnomalyDetector
from fraud_detection.core.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class AnalysisPipeline:
    """完整的分析管道"""

    def __init__(self):
        self.metrics_calculator = FinancialMetricsCalculator()
        self.anomaly_detector = AnomalyDetector()
        self.report_generator = ReportGenerator()

    def run_analysis(
        self,
        ticker: str,
        company_name: str,
        current_metrics: Dict[str, float],
        previous_metrics: Dict[str, Optional[Dict[str, float]]] = None
    ) -> Dict[str, Any]:
        """
        运行完整的欺诈检测分析

        Args:
            ticker: 股票代码
            company_name: 公司名称
            current_metrics: 当期财务指标
            previous_metrics: 上期财务指标

        Returns:
            完整的分析结果
        """
        logger.info(f"Starting analysis for {ticker}: {company_name}")

        result = {
            'metadata': {
                'ticker': ticker,
                'company_name': company_name
            }
        }

        try:
            # Step 1: 计算基础财务比率
            logger.debug("Calculating financial metrics...")
            result['profitability'] = self.metrics_calculator.calculate_profitability_metrics(
                current_metrics
            )
            result['liquidity'] = self.metrics_calculator.calculate_liquidity_metrics(
                current_metrics
            )
            result['solvency'] = self.metrics_calculator.calculate_solvency_metrics(
                current_metrics
            )
            result['efficiency'] = self.metrics_calculator.calculate_efficiency_metrics(
                current_metrics
            )
            result['cash_cycle'] = self.metrics_calculator.calculate_cash_cycle_metrics(
                current_metrics
            )

            # Step 2: 计算Piotroski F-Score
            logger.debug("Calculating Piotroski F-Score...")
            piotroski_inputs = {
                'roa_current': result['profitability'].get('roa', 0),
                'roa_previous': self._get_previous_metric(
                    previous_metrics, 'roa', 'profitability'
                ),
                'cfo_current': current_metrics.get('operating_cash_flow', 0),
                'leverage_current': result['solvency'].get('debt_ratio', 0),
                'leverage_previous': self._get_previous_metric(
                    previous_metrics, 'debt_ratio', 'solvency'
                ),
                'current_ratio_current': result['liquidity'].get('current_ratio', 0),
                'current_ratio_previous': self._get_previous_metric(
                    previous_metrics, 'current_ratio', 'liquidity'
                ),
                'shares_current': current_metrics.get('shares_outstanding', 0),
                'shares_previous': self._get_previous_metric(
                    previous_metrics, 'shares_outstanding'
                ),
                'gross_margin_current': result['profitability'].get('gross_margin', 0),
                'gross_margin_previous': self._get_previous_metric(
                    previous_metrics, 'gross_margin', 'profitability'
                ),
                'asset_turnover_current': result['efficiency'].get('asset_turnover', 0),
                'asset_turnover_previous': self._get_previous_metric(
                    previous_metrics, 'asset_turnover', 'efficiency'
                )
            }
            result['piotroski_score'] = self.metrics_calculator.calculate_piotroski_fscore(
                piotroski_inputs
            )

            # Step 3: 计算欺诈F-Score
            logger.debug("Calculating Fraud F-Score...")
            fraud_inputs = {
                'rsst_accruals': current_metrics.get('rsst_accruals', 0),
                'receivables_growth': current_metrics.get('receivables_growth', 0),
                'inventory_growth': current_metrics.get('inventory_growth', 0),
                'soft_assets_ratio': current_metrics.get('soft_assets_ratio', 0),
                'cash_sales_divergence': current_metrics.get('cash_sales_divergence', 0),
                'roa_deterioration': current_metrics.get('roa_deterioration', 0),
                'refinancing_activity': current_metrics.get('refinancing_activity', 0),
                'abnormal_employee_change': current_metrics.get('abnormal_employee_change', 0),
                'operating_lease_growth': current_metrics.get('operating_lease_growth', 0)
            }
            result['fraud_metrics'] = self.metrics_calculator.calculate_fraud_fscore(
                fraud_inputs
            )

            # Step 4: 计算情感评分
            if 'audit_opinion' in current_metrics or 'negative_news' in current_metrics:
                logger.debug("Calculating sentiment score...")
                text = (
                    current_metrics.get('audit_opinion', '') +
                    ' ' +
                    current_metrics.get('negative_news', '')
                )
                result['sentiment'] = self.metrics_calculator.calculate_sentiment_score(text)

            # Step 5: 检测异常并计算综合风险
            logger.debug("Detecting anomalies...")
            previous_current = previous_metrics or {} if isinstance(previous_metrics, dict) else {}
            result['anomalies'] = self.anomaly_detector.detect_anomalies(
                current_metrics,
                previous_current,
                result['fraud_metrics'].get('score', 0),
                result['piotroski_score'].get('score', 0)
            )

            # Step 6: 生成报告
            logger.debug("Generating report...")
            result['all_metrics'] = {
                'profitability': result['profitability'],
                'liquidity': result['liquidity'],
                'solvency': result['solvency'],
                'efficiency': result['efficiency'],
                'cash_cycle': result['cash_cycle']
            }

            report = self.report_generator.generate_comprehensive_report(
                ticker, company_name, result
            )
            result['report'] = report

            logger.info(f"Analysis completed for {ticker}")
            return result

        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}", exc_info=True)
            raise

    def _get_previous_metric(
        self,
        previous_metrics: Optional[Dict],
        metric_name: str,
        category: Optional[str] = None
    ) -> float:
        """获取上期指标值"""
        if not previous_metrics:
            return 0.0

        if isinstance(previous_metrics, dict):
            if category:
                if category in previous_metrics:
                    return previous_metrics[category].get(metric_name, 0.0)
            else:
                return previous_metrics.get(metric_name, 0.0)

        return 0.0

    def generate_html_report(
        self,
        analysis_result: Dict[str, Any],
        output_path: str
    ) -> str:
        """生成HTML报告"""
        report = analysis_result.get('report', {})
        return self.report_generator.generate_html_dashboard(report, output_path)


# 便捷函数
def run_fraud_detection(
    ticker: str,
    company_name: str,
    current_metrics: Dict[str, float],
    previous_metrics: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    快速运行欺诈检测

    Args:
        ticker: 股票代码
        company_name: 公司名称
        current_metrics: 当期财务指标
        previous_metrics: 上期财务指标

    Returns:
        分析结果
    """
    pipeline = AnalysisPipeline()
    return pipeline.run_analysis(ticker, company_name, current_metrics, previous_metrics)
