from setuptools import setup, find_packages

setup(
    name="fun-facts-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "redis",
        "mistralai",
        "pydantic",
        "python-dateutil",
        "PyYAML",
    ],
)
