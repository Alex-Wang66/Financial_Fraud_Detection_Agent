"""
Fraud Detection Package
"""

from .core import (
    FinancialMetricsCalculator,
    AnomalyDetector,
    ReportGenerator,
    AnalysisPipeline,
    run_fraud_detection,
    DataFetcher,
    fetch_financial_report,
    KeyIndicatorExtractor,
    ExtractedIndicators,
    ExtractorBackend,
    extract_key_indicators,
    extract_from_dict
)

__version__ = '2.0.2'
__author__ = 'Alex Wang'

__all__ = [
    'FinancialMetricsCalculator',
    'AnomalyDetector',
    'ReportGenerator',
    'AnalysisPipeline',
    'run_fraud_detection',
    'DataFetcher',
    'fetch_financial_report',
    'KeyIndicatorExtractor',
    'ExtractedIndicators',
    'ExtractorBackend',
    'extract_key_indicators',
    'extract_from_dict'
]
