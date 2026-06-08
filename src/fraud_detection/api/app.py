"""
Flask API Server for Fraud Detection
欺诈检测Flask API服务
"""

import logging
import json
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound
from fraud_detection.core import AnalysisPipeline
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 初始化分析管道
pipeline = AnalysisPipeline()


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_fraud():
    """
    分析财务欺诈风险

    Request JSON:
    {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "current_metrics": {...},
        "previous_metrics": {...}  // optional
    }
    """
    try:
        data = request.get_json()

        # 验证必需字段
        if not data:
            return jsonify({'error': 'Request body is empty'}), BadRequest.code

        required_fields = ['ticker', 'company_name', 'current_metrics']
        missing_fields = [f for f in required_fields if f not in data]

        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), BadRequest.code

        ticker = data['ticker']
        company_name = data['company_name']
        current_metrics = data['current_metrics']
        previous_metrics = data.get('previous_metrics')

        # 运行分析
        logger.info(f"Running analysis for {ticker}: {company_name}")
        result = pipeline.run_analysis(
            ticker, company_name, current_metrics, previous_metrics
        )

        # 返回结果
        return jsonify({
            'success': True,
            'ticker': ticker,
            'company_name': company_name,
            'risk_score': result['anomalies'].get('risk_score', 0),
            'risk_level': result['anomalies'].get('risk_level', 'Unknown'),
            'fraud_score': result['fraud_metrics'].get('score', 0),
            'piotroski_score': result['piotroski_score'].get('score', 0),
            'top_5_risk_factors': [
                {
                    'name': f.get('name'),
                    'description': f.get('description'),
                    'severity': f.get('severity'),
                    'contribution': f.get('contribution')
                }
                for f in result['anomalies'].get('top_5_factors', [])
            ],
            'summary': result['report'].get('executive_summary', {}).get('summary', '')
        }), 200

    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({'error': str(e)}), BadRequest.code
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/analyze/detailed', methods=['POST'])
def analyze_fraud_detailed():
    """
    获取详细分析结果
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is empty'}), BadRequest.code

        required_fields = ['ticker', 'company_name', 'current_metrics']
        missing_fields = [f for f in required_fields if f not in data]

        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), BadRequest.code

        ticker = data['ticker']
        company_name = data['company_name']
        current_metrics = data['current_metrics']
        previous_metrics = data.get('previous_metrics')

        # 运行分析
        logger.info(f"Running detailed analysis for {ticker}: {company_name}")
        result = pipeline.run_analysis(
            ticker, company_name, current_metrics, previous_metrics
        )

        # 返回完整结果
        return jsonify({
            'success': True,
            'ticker': ticker,
            'company_name': company_name,
            'analysis': {
                'anomalies': result['anomalies'],
                'fraud_metrics': result['fraud_metrics'],
                'piotroski_score': result['piotroski_score'],
                'profitability': result['profitability'],
                'liquidity': result['liquidity'],
                'solvency': result['solvency'],
                'efficiency': result['efficiency'],
                'cash_cycle': result['cash_cycle']
            },
            'report': result['report']
        }), 200

    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({'error': str(e)}), BadRequest.code
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/analyze/html', methods=['POST'])
def analyze_and_generate_html():
    """
    分析并生成HTML报告
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is empty'}), BadRequest.code

        required_fields = ['ticker', 'company_name', 'current_metrics']
        missing_fields = [f for f in required_fields if f not in data]

        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), BadRequest.code

        ticker = data['ticker']
        company_name = data['company_name']
        current_metrics = data['current_metrics']
        previous_metrics = data.get('previous_metrics')

        # 运行分析
        logger.info(f"Running analysis and generating HTML for {ticker}")
        result = pipeline.run_analysis(
            ticker, company_name, current_metrics, previous_metrics
        )

        # 生成HTML报告
        html_dir = os.path.join(os.path.dirname(__file__), '../..', 'reports')
        os.makedirs(html_dir, exist_ok=True)

        html_filename = f'{ticker}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        html_path = os.path.join(html_dir, html_filename)

        pipeline.generate_html_report(result, html_path)

        return jsonify({
            'success': True,
            'ticker': ticker,
            'company_name': company_name,
            'html_file': html_filename,
            'html_path': html_path,
            'risk_level': result['anomalies'].get('risk_level', 'Unknown'),
            'risk_score': result['anomalies'].get('risk_score', 0)
        }), 200

    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({'error': str(e)}), BadRequest.code
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/metrics/piotroski', methods=['POST'])
def calculate_piotroski():
    """计算Piotroski F-Score"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is empty'}), BadRequest.code

        from fraud_detection.core import FinancialMetricsCalculator
        calc = FinancialMetricsCalculator()

        result = calc.calculate_piotroski_fscore(data)

        return jsonify({
            'success': True,
            'piotroski_score': result
        }), 200

    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/fraud', methods=['POST'])
def calculate_fraud_score():
    """计算欺诈F-Score"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is empty'}), BadRequest.code

        from fraud_detection.core import FinancialMetricsCalculator
        calc = FinancialMetricsCalculator()

        result = calc.calculate_fraud_fscore(data)

        return jsonify({
            'success': True,
            'fraud_score': result
        }), 200

    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API文档"""
    docs = """
    <html>
    <head>
        <title>Financial Fraud Detection API Documentation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #2196F3; }
            h2 { color: #666; margin-top: 30px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { display: inline-block; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; }
            .post { background: #4CAF50; }
            .get { background: #2196F3; }
            code { background: #eee; padding: 2px 5px; border-radius: 3px; }
            pre { background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>财务欺诈检测 API 文档</h1>

        <h2>基本信息</h2>
        <p>API 版本: 2.0.0</p>
        <p>基础 URL: /api</p>

        <h2>端点</h2>

        <div class="endpoint">
            <span class="method get">GET</span> <code>/health</code>
            <p>健康检查</p>
            <p><strong>响应:</strong></p>
            <pre>{"status": "healthy", "timestamp": "...", "version": "2.0.0"}</pre>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span> <code>/analyze</code>
            <p>执行欺诈检测分析</p>
            <p><strong>请求:</strong></p>
            <pre>{
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "current_metrics": {...},
    "previous_metrics": {...}  // 可选
}</pre>
            <p><strong>响应:</strong></p>
            <pre>{
    "success": true,
    "risk_score": 42.5,
    "risk_level": "Medium",
    "fraud_score": 4,
    "piotroski_score": 7,
    "top_5_risk_factors": [...]
}</pre>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span> <code>/analyze/detailed</code>
            <p>获取详细分析结果</p>
            <p><strong>请求:</strong> 同 /analyze</p>
            <p><strong>响应:</strong> 包含所有分析指标的完整报告</p>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span> <code>/analyze/html</code>
            <p>分析并生成HTML报告</p>
            <p><strong>请求:</strong> 同 /analyze</p>
            <p><strong>响应:</strong></p>
            <pre>{
    "success": true,
    "html_file": "AAPL_20240101_120000.html",
    "html_path": "/path/to/report/",
    "risk_level": "High"
}</pre>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span> <code>/metrics/piotroski</code>
            <p>计算Piotroski F-Score</p>
            <p><strong>请求:</strong> 财务指标字典</p>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span> <code>/metrics/fraud</code>
            <p>计算欺诈F-Score</p>
            <p><strong>请求:</strong> 欺诈指标字典</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(docs)


@app.errorhandler(400)
def bad_request(error):
    """处理400错误"""
    return jsonify({'error': 'Bad Request', 'message': str(error.description)}), 400


@app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """处理500错误"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
