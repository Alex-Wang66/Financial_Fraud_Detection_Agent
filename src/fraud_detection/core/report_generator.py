"""
Report Generation System
报告生成系统
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
from jinja2 import Template

logger = logging.getLogger(__name__)


class ReportGenerator:
    """生成财务欺诈检测报告"""

    def generate_comprehensive_report(
        self,
        ticker: str,
        company_name: str,
        analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成综合分析报告

        Args:
            ticker: 股票代码
            company_name: 公司名称
            analysis_result: 分析结果

        Returns:
            完整的报告数据
        """
        report = {
            'metadata': {
                'ticker': ticker,
                'company_name': company_name,
                'report_date': datetime.now().isoformat(),
                'report_version': '1.0'
            },
            'executive_summary': self._generate_executive_summary(analysis_result),
            'risk_assessment': self._generate_risk_assessment(analysis_result),
            'fraud_indicators': self._generate_fraud_indicators(analysis_result),
            'financial_health': self._generate_financial_health(analysis_result),
            'recommendations': self._generate_recommendations(analysis_result),
            'detailed_metrics': analysis_result
        }
        return report

    def _generate_executive_summary(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """生成执行摘要"""
        risk_score = analysis.get('anomalies', {}).get('risk_score', 0)
        risk_level = analysis.get('anomalies', {}).get('risk_level', 'Unknown')
        fraud_score = analysis.get('fraud_metrics', {}).get('score', 0)
        piotroski_score = analysis.get('piotroski_score', {}).get('score', 0)

        summary = f"""
公司 {analysis.get('company_name', 'N/A')} 的财务欺诈风险评估表明：

总体风险等级：{risk_level}
综合风险评分：{risk_score:.1f}/100

关键指标：
- 欺诈F-Score: {fraud_score}/9 (风险指数)
- Piotroski F-Score: {piotroski_score}/9 (财务质量)

该评估基于对公司财务报表、现金流分析、运营指标和市场信息的综合分析。
"""
        return {
            'summary': summary.strip(),
            'risk_level': risk_level,
            'risk_score': risk_score,
            'fraud_score': fraud_score,
            'piotroski_score': piotroski_score
        }

    def _generate_risk_assessment(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成风险评估"""
        anomalies = analysis.get('anomalies', {})
        top_factors = anomalies.get('top_5_factors', [])

        assessment = {
            'overall_risk_score': anomalies.get('risk_score', 0),
            'risk_level': anomalies.get('risk_level', 'Unknown'),
            'total_risk_factors': anomalies.get('total_factors', 0),
            'score_components': anomalies.get('score_components', {}),
            'top_risk_factors': []
        }

        for i, factor in enumerate(top_factors, 1):
            assessment['top_risk_factors'].append({
                'rank': i,
                'name': factor.get('name', ''),
                'description': factor.get('description', ''),
                'severity': factor.get('severity', 'unknown'),
                'contribution': factor.get('contribution', 0)
            })

        return assessment

    def _generate_fraud_indicators(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成欺诈风险指标"""
        fraud = analysis.get('fraud_metrics', {})
        risk_factors = fraud.get('risk_factors', {})

        indicators = {
            'fraud_fscore': fraud.get('score', 0),
            'flagged_factors_count': fraud.get('flagged_count', 0),
            'risk_factors': []
        }

        # 只列出被标记的风险因子
        for factor_name, factor_data in risk_factors.items():
            if factor_data.get('flagged'):
                indicators['risk_factors'].append({
                    'factor_name': factor_name,
                    'value': factor_data.get('value', 0),
                    'threshold': factor_data.get('threshold', 'N/A'),
                    'flagged': True,
                    'interpretation': self._interpret_fraud_factor(factor_name, factor_data)
                })

        return indicators

    def _generate_financial_health(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成财务健康评估"""
        piotroski = analysis.get('piotroski_score', {})
        metrics = analysis.get('all_metrics', {})

        health = {
            'piotroski_fscore': piotroski.get('score', 0),
            'financial_quality': self._rate_quality(piotroski.get('score', 0)),
            'key_metrics': {
                'roa': metrics.get('profitability', {}).get('roa', 0),
                'roe': metrics.get('profitability', {}).get('roe', 0),
                'net_margin': metrics.get('profitability', {}).get('net_margin', 0),
                'current_ratio': metrics.get('liquidity', {}).get('current_ratio', 0),
                'debt_ratio': metrics.get('solvency', {}).get('debt_ratio', 0),
                'asset_turnover': metrics.get('efficiency', {}).get('asset_turnover', 0)
            },
            'strengths': self._identify_strengths(piotroski),
            'weaknesses': self._identify_weaknesses(piotroski)
        }

        return health

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """生成建议"""
        recommendations = []
        risk_level = analysis.get('anomalies', {}).get('risk_level', 'Low')
        top_factors = analysis.get('anomalies', {}).get('top_5_factors', [])

        if risk_level == 'High':
            recommendations.append({
                'priority': 'Critical',
                'recommendation': '建议进行深入的尽职调查和财务审计',
                'reason': '综合风险评分高，存在显著的欺诈风险'
            })
        elif risk_level == 'Medium':
            recommendations.append({
                'priority': 'High',
                'recommendation': '建议加强财务监控和内部审计',
                'reason': '存在中等风险，需要进一步监测'
            })

        # 基于主要风险因子的具体建议
        for factor in top_factors[:3]:
            rec = self._get_factor_recommendation(factor)
            if rec:
                recommendations.append(rec)

        return recommendations

    def _interpret_fraud_factor(self, factor_name: str, factor_data: Dict) -> str:
        """解释欺诈因子"""
        interpretations = {
            'high_accruals': '公司的应计收益比例较高，可能存在盈利质量问题',
            'receivables_growth': '应收账款增长过快，可能存在激进的收入确认政策',
            'inventory_growth': '库存快速增长，可能存在库存囤积或销售困难',
            'high_soft_assets': '软资产（无形资产）比例高，容易被操纵',
            'cash_sales_divergence': '销售增长与现金流不匹配，可能存在虚假收入',
            'roa_deterioration': '资产回报率下降，可能激励管理层财务操纵',
            'refinancing_activity': '融资活动增加，表明可能存在流动性压力',
            'abnormal_employee_change': '员工变化异常，可能反映运营变化',
            'operating_lease_growth': '经营性租赁增长，可能隐瞒负债'
        }
        return interpretations.get(factor_name, '需要进一步分析')

    def _get_factor_recommendation(self, factor: Dict) -> Dict[str, str]:
        """获取针对特定风险因子的建议"""
        recommendations_map = {
            'cash_cycle_critical': {
                'priority': 'High',
                'recommendation': '加强现金管理，优化应收和应付账款周期',
                'reason': '现金周期过长，影响流动性'
            },
            'high_debt_ratio_critical': {
                'priority': 'High',
                'recommendation': '制定债务削减计划，改善资本结构',
                'reason': '债务比率过高，存在偿债风险'
            },
            'high_receivable_days_critical': {
                'priority': 'Medium',
                'recommendation': '加强应收账款管理，加速回款',
                'reason': '应收账款周期过长，可能影响现金流'
            },
            'negative_growth_critical': {
                'priority': 'High',
                'recommendation': '分析利润下滑原因，制定改善计划',
                'reason': '净利润严重下滑，存在运营风险'
            }
        }
        return recommendations_map.get(factor.get('name'), None)

    def _rate_quality(self, piotroski_score: float) -> str:
        """评价财务质量"""
        if piotroski_score >= 8:
            return 'Excellent'
        elif piotroski_score >= 6:
            return 'Good'
        elif piotroski_score >= 4:
            return 'Fair'
        else:
            return 'Poor'

    def _identify_strengths(self, piotroski: Dict) -> List[str]:
        """识别财务优势"""
        strengths = []
        details = piotroski.get('details', {})

        if details.get('roa_positive'):
            strengths.append('正回报率')
        if details.get('cfo_positive'):
            strengths.append('正运营现金流')
        if details.get('liquidity_improved'):
            strengths.append('流动性改善')
        if details.get('leverage_decreased'):
            strengths.append('杠杆降低')

        return strengths if strengths else ['无明显优势']

    def _identify_weaknesses(self, piotroski: Dict) -> List[str]:
        """识别财务弱点"""
        weaknesses = []
        details = piotroski.get('details', {})

        if not details.get('roa_positive'):
            weaknesses.append('负回报率')
        if not details.get('cfo_positive'):
            weaknesses.append('负运营现金流')
        if not details.get('liquidity_improved'):
            weaknesses.append('流动性恶化')
        if not details.get('leverage_decreased'):
            weaknesses.append('杠杆增加')

        return weaknesses if weaknesses else ['无明显弱点']

    def generate_html_dashboard(self, report: Dict[str, Any], output_path: str) -> str:
        """
        生成HTML仪表板

        Args:
            report: 报告数据
            output_path: 输出路径

        Returns:
            HTML文件路径
        """
        metadata = report.get('metadata', {})
        summary = report.get('executive_summary', {})
        risk = report.get('risk_assessment', {})
        fraud = report.get('fraud_indicators', {})
        health = report.get('financial_health', {})

        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财务欺诈检测报告 - {{ ticker }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; color: #333; }
        .container { max-width: 1200px; margin: 20px auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        header { border-bottom: 3px solid #2196F3; padding-bottom: 20px; margin-bottom: 30px; }
        h1 { color: #2196F3; margin-bottom: 10px; }
        .meta { color: #666; font-size: 0.9em; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; background: #f9f9f9; }
        .card h3 { color: #2196F3; margin-bottom: 15px; font-size: 1.1em; }
        .metric { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
        .metric:last-child { border-bottom: none; }
        .metric-label { font-weight: 500; }
        .metric-value { font-weight: bold; color: #2196F3; }
        .risk-high { color: #f44336; }
        .risk-medium { color: #ff9800; }
        .risk-low { color: #4caf50; }
        .score-box { text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; }
        .score-box .value { font-size: 2.5em; font-weight: bold; }
        .score-box .label { font-size: 0.9em; margin-top: 10px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th { background: #2196F3; color: white; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f5f5f5; }
        .recommendation { background: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 10px 0; }
        .rec-priority-high { border-left-color: #f44336; }
        .rec-priority-medium { border-left-color: #ff9800; }
        footer { margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>财务欺诈检测报告</h1>
            <div class="meta">
                <p><strong>公司：</strong> {{ company_name }} ({{ ticker }})</p>
                <p><strong>报告日期：</strong> {{ report_date }}</p>
            </div>
        </header>

        <section class="grid">
            <div class="score-box">
                <div class="label">综合风险评分</div>
                <div class="value">{{ summary.risk_score|round(1) }}</div>
                <div class="label">/ 100</div>
            </div>
            <div class="score-box" style="background: linear-gradient(135deg, {{ risk_color }} 0%, {{ risk_color_dark }} 100%);">
                <div class="label">风险等级</div>
                <div class="value">{{ summary.risk_level }}</div>
            </div>
        </section>

        <section class="card">
            <h3>执行摘要</h3>
            <p>{{ summary.summary }}</p>
        </section>

        <section class="grid">
            <div class="card">
                <h3>欺诈指标</h3>
                <div class="metric">
                    <span class="metric-label">欺诈F-Score</span>
                    <span class="metric-value">{{ summary.fraud_score }}/9</span>
                </div>
                <div class="metric">
                    <span class="metric-label">被标记风险因子</span>
                    <span class="metric-value">{{ fraud.flagged_factors_count }}</span>
                </div>
            </div>
            <div class="card">
                <h3>财务质量</h3>
                <div class="metric">
                    <span class="metric-label">Piotroski F-Score</span>
                    <span class="metric-value">{{ summary.piotroski_score }}/9</span>
                </div>
                <div class="metric">
                    <span class="metric-label">财务质量评级</span>
                    <span class="metric-value">{{ health.financial_quality }}</span>
                </div>
            </div>
        </section>

        <section class="card">
            <h3>主要风险因子 (Top 5)</h3>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>风险因子</th>
                        <th>严重程度</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
                    {% for factor in risk.top_risk_factors %}
                    <tr>
                        <td>{{ factor.rank }}</td>
                        <td>{{ factor.name }}</td>
                        <td class="risk-{{ factor.severity|lower }}">{{ factor.severity|upper }}</td>
                        <td>{{ factor.description }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>

        <section class="card">
            <h3>关键财务指标</h3>
            <div class="metric">
                <span class="metric-label">总资产收益率 (ROA)</span>
                <span class="metric-value">{{ "%.2f%%"|format(health.key_metrics.roa * 100) }}</span>
            </div>
            <div class="metric">
                <span class="metric-label">股东权益收益率 (ROE)</span>
                <span class="metric-value">{{ "%.2f%%"|format(health.key_metrics.roe * 100) }}</span>
            </div>
            <div class="metric">
                <span class="metric-label">净利率</span>
                <span class="metric-value">{{ "%.2f%%"|format(health.key_metrics.net_margin * 100) }}</span>
            </div>
            <div class="metric">
                <span class="metric-label">流动比率</span>
                <span class="metric-value">{{ "%.2f"|format(health.key_metrics.current_ratio) }}</span>
            </div>
            <div class="metric">
                <span class="metric-label">债务比率</span>
                <span class="metric-value">{{ "%.2f%%"|format(health.key_metrics.debt_ratio * 100) }}</span>
            </div>
            <div class="metric">
                <span class="metric-label">资产周转率</span>
                <span class="metric-value">{{ "%.2f"|format(health.key_metrics.asset_turnover) }}</span>
            </div>
        </section>

        <section class="card">
            <h3>财务优势与弱点</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="color: #4caf50; margin-bottom: 10px;">优势</h4>
                    <ul style="list-style: none;">
                        {% for strength in health.strengths %}
                        <li style="padding: 5px 0;">✓ {{ strength }}</li>
                        {% endfor %}
                    </ul>
                </div>
                <div>
                    <h4 style="color: #f44336; margin-bottom: 10px;">弱点</h4>
                    <ul style="list-style: none;">
                        {% for weakness in health.weaknesses %}
                        <li style="padding: 5px 0;">✗ {{ weakness }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </section>

        <section class="card">
            <h3>建议</h3>
            {% for rec in recommendations %}
            <div class="recommendation rec-priority-{{ rec.priority|lower }}">
                <strong>[{{ rec.priority|upper }}]</strong> {{ rec.recommendation }}<br>
                <small style="color: #666;">原因: {{ rec.reason }}</small>
            </div>
            {% endfor %}
        </section>

        <footer>
            <p>本报告由财务欺诈检测系统自动生成，仅供参考。建议结合人工分析和专业意见使用。</p>
            <p>Report Version: {{ report_version }} | Generated: {{ report_date }}</p>
        </footer>
    </div>
</body>
</html>
        """

        template = Template(html_template)

        # 确定风险颜色
        risk_level = summary.get('risk_level', 'Low')
        risk_colors = {
            'Low': '#4caf50',
            'Medium': '#ff9800',
            'High': '#f44336'
        }
        risk_color = risk_colors.get(risk_level, '#2196F3')
        risk_color_dark = risk_colors.get(risk_level, '#1976d2')

        html_content = template.render(
            ticker=metadata.get('ticker', 'N/A'),
            company_name=metadata.get('company_name', 'N/A'),
            report_date=metadata.get('report_date', 'N/A'),
            report_version=metadata.get('report_version', '1.0'),
            summary=summary,
            risk=risk,
            fraud=fraud,
            health=health,
            recommendations=report.get('recommendations', []),
            risk_color=risk_color,
            risk_color_dark=risk_color_dark
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_path
