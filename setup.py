from setuptools import setup

setup(
    name='RPNCalculator',
    version='1.4.0',
    description='Interactive Forth-like calculator',
    author='Phil Hanna',
    author_email='ph1204@gmail.com',
    license='MIT',
    packages=['evaluator', 'evaluator.test'],
    url='https://github.com/philhanna/RPNCalculator',
    zip_safe=False
)
