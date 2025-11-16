"""
Setup file for Cryptocurrency Data Server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crypto-data-server",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Production-ready cryptocurrency data server with real-time streaming, caching, and analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crypto-data-server",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "ccxt==4.0.36",
        "cachetools==5.3.2",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1",
        "httpx==0.25.1",
        "websockets==12.0",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
    ],
    extras_require={
        "dev": [
            "black==23.11.0",
            "flake8==6.1.0",
            "mypy==1.7.0",
            "pytest-cov==4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "crypto-server=main:app",
        ],
    },
)
