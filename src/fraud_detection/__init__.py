"""
Fraud Detection Package
"""

from .core import (
    FinancialMetricsCalculator,
    AnomalyDetector,
    ReportGenerator,
    AnalysisPipeline,
    run_fraud_detection
)

__version__ = '2.0.0'
__author__ = 'Alex Wang'

__all__ = [
    'FinancialMetricsCalculator',
    'AnomalyDetector',
    'ReportGenerator',
    'AnalysisPipeline',
    'run_fraud_detection'
]
