from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="bqq",
    version="0.0.1",
    description="BigQuery query",
    long_description=long_description,
    author="Martin Tupy",
    author_email="id@martintupy.com",
    packages=find_packages(),
    install_requires=["google-cloud-bigquery", "Click", "prettytable"],
    entry_points={"console_scripts": ["bqq = bqq:cli"]},
)
