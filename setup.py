import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='qastle',
                 version=0.8,
                 description='Query AST Language Expressions',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(exclude=['tests']),
                 install_requires=['lark-parser>=0.6.5'],
                 package_data={'qastle': ['syntax.lark']},
                 author='Mason Proffitt',
                 author_email='masonlp@uw.edu',
                 url='https://github.com/iris-hep/qastle')
