from setuptools import setup, find_packages

setup(
    name="gai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "googlesearch-python"
    ],
    author="other",
    description="A chatbot that fetches responses from Google, Reddit, and code websites.",
    url="https://github.com/support-bot101/Gai",
)
