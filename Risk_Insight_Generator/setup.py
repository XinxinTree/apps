from setuptools import setup, find_packages

setup(
    name="risk_signal_analyzer",
    version="0.1.0",
    description="Tool for analyzing incident reports and system logs to extract risk signals",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "python-multipart>=0.0.6",
        "pandas>=1.3.0",
        "nltk>=3.6.0",
        "numpy>=1.19.0",
        "scikit-learn>=0.24.0",
        "python-dateutil>=2.8.0",
        "streamlit>=1.12.0",
        "plotly>=5.3.0"
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'risk_analyzer=app:main',
        ],
    },
)
