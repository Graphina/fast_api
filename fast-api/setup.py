from os import path

from setuptools import find_packages, setup

absolute_path = path.abspath(path.dirname(__file__))


def get_file_data(filename):
    with open(path.join(absolute_path, filename), encoding="utf-8") as f:
        file_data = f.read()
    return file_data


setup(
    name="FASTApi",
    version="0.0.2",
    description="FASTApi API",
    long_description=get_file_data("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

    ],
    packages=find_packages(),
    install_requires=get_file_data("requirements.txt").split("\n"),
    python_requires=">=3.5",
)
