from setuptools import setup, find_packages

setup(
    name="common",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "aiosignal",
        "annotated-types",
        "anyio",
        "attrs",
        "azure-core",
        "azure-cosmos",
        "certifi",
        "charset-normalizer",
        "distro",
        "frozenlist",
        "groq",
        "h11",
        "httpcore",
        "httpx",
        "idna",
        "jsonpatch",
        "jsonpointer",
        "langchain",
        "langchain-core",
        "langchain-groq",
        "langchain-text-splitters",
        "langsmith",
        "multidict",
        "numpy",
        "orjson",
        "packaging",
        "pydantic",
        "pydantic_core",
        "python-dotenv",
        "PyYAML",
        "requests",
        "setuptools",
        "six",
        "sniffio",
        "SQLAlchemy",
        "tenacity",
        "typing_extensions",
        "urllib3",
        "yarl",
    ],
)
