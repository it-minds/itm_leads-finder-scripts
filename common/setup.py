from setuptools import setup, find_packages

setup(
    name="common",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "azure-cosmos",
    ],
)
