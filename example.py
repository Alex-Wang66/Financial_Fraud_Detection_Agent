"""
Example usage of Financial Fraud Detection System
财务欺诈检测系统的使用示例
"""

import json
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from fraud_detection.core import AnalysisPipeline


def main():
    """主函数"""

    # 初始化分析管道
    pipeline = AnalysisPipeline()

    # 示例 1：Apple Inc. 的财务数据
    print("=" * 80)
    print("示例：Apple Inc. 的财务欺诈风险分析")
    print("=" * 80)

    # 当期财务指标（2024年）
    apple_current = {
        'ticker': 'AAPL',
        'company_name': 'Apple Inc.',

        # 收入和利润
        'revenue': 383285000000,  # $383.3B
        'net_income': 93736000000,  # $93.7B
        'gross_profit': 169961000000,  # $170.0B
        'operating_income': 111437000000,  # $111.4B
        'ebitda': 130541000000,  # $130.5B

        # 资产和负债
        'total_assets': 348988000000,  # $349.0B
        'total_liabilities': 147177000000,  # $147.2B
        'shareholders_equity': 201811000000,  # $201.8B
        'total_debt': 108949000000,  # $108.9B

        # 流动资产和流动负债
        'current_assets': 145071000000,  # $145.1B
        'current_liabilities': 111299000000,  # $111.3B
        'cash': 39572000000,  # $39.6B
        'inventory': 6331000000,  # $6.3B
        'accounts_receivable': 29086000000,  # $29.1B

        # 现金流
        'operating_cash_flow': 119437000000,  # $119.4B
        'cost_of_goods_sold': 214309000000,  # $214.3B

        # 计算的指标
        'cash_cycle': 20,  # 日数
        'receivable_days': 28,
        'inventory_days': 10,
        'payable_days': 85,

        # 欺诈指标
        'rsst_accruals': 0.05,  # 5%
        'receivables_growth': 0.08,  # 8%
        'inventory_growth': 0.05,  # 5%
        'soft_assets_ratio': 0.35,  # 35%
        'cash_sales_divergence': 0.02,  # 2%
        'roa_deterioration': 0.01,  # 1% 改善
        'refinancing_activity': 0,
        'abnormal_employee_change': 0.02,  # 2% 变化
        'operating_lease_growth': 0.05,  # 5%

        # 审计意见
        'audit_opinion': 'Unqualified',
        'negative_news_count': 1,

        # 其他
        'shares_outstanding': 15775000000,
        'interest_expense': 2931000000,
        'ebit': 114368000000
    }

    # 上期财务指标（2023年）
    apple_previous = {
        'revenue': 394328000000,  # $394.3B
        'net_income': 96995000000,  # $97.0B
        'gross_profit': 170782000000,  # $170.8B
        'operating_income': 120656000000,  # $120.7B
        'total_assets': 352755000000,  # $352.8B
        'shareholders_equity': 202441000000,  # $202.4B
        'current_assets': 143713000000,  # $143.7B
        'current_liabilities': 123337000000,  # $123.3B
        'operating_cash_flow': 110543000000,  # $110.5B
        'shares_outstanding': 15812000000,  # 更多股份
    }

    # 运行分析
    result = pipeline.run_analysis(
        ticker='AAPL',
        company_name='Apple Inc.',
        current_metrics=apple_current,
        previous_metrics={
            'profitability': {'roa': 0.275},  # 上期ROA
            'solvency': {'debt_ratio': 0.310},  # 上期债务比率
            'liquidity': {'current_ratio': 1.165},  # 上期流动比率
            'efficiency': {'asset_turnover': 1.118},  # 上期资产周转率
        }
    )

    # 输出结果
    print("\n【执行摘要】")
    summary = result['report']['executive_summary']
    print(summary['summary'])

    print("\n【主要风险指标】")
    print(f"综合风险评分: {result['anomalies']['risk_score']:.1f}/100")
    print(f"风险等级: {result['anomalies']['risk_level']}")
    print(f"欺诈F-Score: {result['fraud_metrics']['score']}/9+")
    print(f"Piotroski F-Score: {result['piotroski_score']['score']}/9")

    print("\n【Top 5 风险因子】")
    for i, factor in enumerate(result['anomalies']['top_5_factors'][:5], 1):
        print(f"{i}. {factor['name']} [{factor['severity'].upper()}]")
        print(f"   {factor['description']}")
        print(f"   贡献: {factor['contribution']:.1f}")

    print("\n【关键财务指标】")
    metrics = result['all_metrics']
    print(f"总资产收益率 (ROA): {metrics['profitability']['roa']:.2%}")
    print(f"股东权益收益率 (ROE): {metrics['profitability']['roe']:.2%}")
    print(f"净利率: {metrics['profitability']['net_margin']:.2%}")
    print(f"流动比率: {metrics['liquidity']['current_ratio']:.2f}")
    print(f"债务比率: {metrics['solvency']['debt_ratio']:.2%}")
    print(f"现金周期: {metrics['cash_cycle']['cash_cycle']:.0f} 天")

    print("\n【建议】")
    for rec in result['report']['recommendations'][:3]:
        print(f"[{rec['priority'].upper()}] {rec['recommendation']}")
        print(f"原因: {rec['reason']}\n")

    # 生成HTML报告
    print("\n【生成HTML报告】")
    html_output = Path('output') / 'AAPL_report.html'
    html_output.parent.mkdir(exist_ok=True)

    html_path = pipeline.generate_html_report(result, str(html_output))
    print(f"✓ HTML报告已生成: {html_path}")

    # 示例 2：另一个公司
    print("\n" + "=" * 80)
    print("示例 2：虚构公司的高风险分析")
    print("=" * 80)

    high_risk_metrics = {
        'revenue': 1000000,
        'net_income': 50000,
        'operating_cash_flow': 30000,  # 现金流较低
        'total_assets': 5000000,
        'total_liabilities': 4000000,  # 高债务
        'shareholders_equity': 1000000,
        'current_assets': 1500000,
        'current_liabilities': 1200000,  # 流动性紧张
        'accounts_receivable': 400000,  # 高应收账款
        'inventory': 600000,  # 高库存

        # 欺诈指标全部偏高
        'rsst_accruals': 0.25,  # 25% - 高
        'receivables_growth': 0.30,  # 30% - 高
        'inventory_growth': 0.25,  # 25% - 高
        'soft_assets_ratio': 0.70,  # 70% - 高
        'cash_sales_divergence': 0.35,  # 35% - 高
        'roa_deterioration': -0.15,  # -15% - 恶化
        'refinancing_activity': 500000,  # 有融资
        'abnormal_employee_change': 0.35,  # 35% - 高
        'operating_lease_growth': 0.30,  # 30% - 高

        'shares_outstanding': 1000000,
        'interest_expense': 150000,
        'ebit': 200000,
        'cash': 50000,
        'cost_of_goods_sold': 600000,
        'gross_profit': 400000,
    }

    result_high_risk = pipeline.run_analysis(
        ticker='TEST',
        company_name='Test High Risk Company',
        current_metrics=high_risk_metrics
    )

    print(f"\n综合风险评分: {result_high_risk['anomalies']['risk_score']:.1f}/100")
    print(f"风险等级: {result_high_risk['anomalies']['risk_level']}")
    print(f"欺诈F-Score: {result_high_risk['fraud_metrics']['score']}/9+")

    print("\n被标记的欺诈因子:")
    for factor_name, factor_data in result_high_risk['fraud_metrics']['risk_factors'].items():
        if factor_data['flagged']:
            print(f"  ✗ {factor_name}: {factor_data['value']:.2%} (阈值: {factor_data['threshold']})")

    print("\n" + "=" * 80)
    print("示例执行完成！")
    print("=" * 80)


if __name__ == '__main__':
    main()
