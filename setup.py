import sys
import setuptools


# Taken from Numba
def _guard_python_version(max_python):
    version_module = None
    try:
        from packaging import version as version_module
    except ImportError:
        try:
            from setuptools._vendor.packaging import version as version_module
        except ImportError:
            pass

    if version_module is None:
        return

    current_python = version_module.parse(".".join(map(str, sys.version_info[:3])))
    max_python = version_module.parse(max_python)

    if not current_python < max_python:
        raise RuntimeError(
            f"Cannot install on Python version {current_python} as Python {max_python}+ is not yet supported."
        )


_guard_python_version(max_python="3.13")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='qastle',
                 version='0.17.0',
                 description='Query AST Language Expressions',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(exclude=['tests']),
                 python_requires=('>=3.8'),
                 install_requires=['lark'],
                 extras_require={'test': ['flake8', 'pytest', 'pytest-cov']},
                 package_data={'qastle': ['syntax.lark']},
                 author='Mason Proffitt',
                 author_email='masonlp@uw.edu',
                 url='https://github.com/iris-hep/qastle')
