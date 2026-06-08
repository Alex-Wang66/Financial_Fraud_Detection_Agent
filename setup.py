"""
Setup configuration for Financial Fraud Detection System
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fraud-detection-system',
    version='2.0.0',
    author='Alex Wang',
    author_email='your.email@example.com',
    description='AI-powered financial fraud detection system using advanced financial metrics and risk scoring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Alex-Wang66/Financial_Fraud_Detection_Agent',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'Flask>=2.3.0',
        'flask-cors>=4.0.0',
        'Jinja2>=3.1.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'requests>=2.31.0',
        'gunicorn>=21.0.0',
        'python-dotenv>=1.0.0'
    ],
    entry_points={
        'console_scripts': [
            'fraud-detection=fraud_detection.cli:main',
        ],
    },
)
