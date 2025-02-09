from setuptools import setup, find_packages

setup(
    name="gai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["googlesearch-python", "requests", "beautifulsoup4"],
)
