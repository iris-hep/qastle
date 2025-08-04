import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qastle",
    version="0.19.0",
    description="Query AST Language Expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=(">=3.8, <3.15"),
    install_requires=["lark"],
    extras_require={"test": ["flake8", "pytest", "pytest-cov"]},
    package_data={"qastle": ["syntax.lark"]},
    author="Mason Proffitt",
    author_email="masonlp@uw.edu",
    url="https://github.com/iris-hep/qastle",
)
