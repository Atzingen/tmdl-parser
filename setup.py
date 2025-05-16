from setuptools import setup, find_packages

setup(
    name="tmdl-parser",
    version="0.1.0",
    description="A Python library to parse and process TMDL (Table Metadata Description Language) files.",
    author="Gustavo von Atzingen",
    author_email="gustavo.von.atzingen@gmail.com",
    url="https://github.com/Atzingen/tmdl-parser",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
