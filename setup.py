import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='qastle',
                 version=0.9,
                 description='Query AST Language Expressions',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(exclude=['tests']),
                 python_requires=('>=2.7, '
                                  '!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <3.10'),
                 install_requires=['lark-parser>=0.6.5'],
                 package_data={'qastle': ['syntax.lark']},
                 author='Mason Proffitt',
                 author_email='masonlp@uw.edu',
                 url='https://github.com/iris-hep/qastle')
