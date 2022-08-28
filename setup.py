from setuptools import setup

setup(
    name='RPNCalculator',
    version='1.6.0',
    package_dir={"": "evaluator"},
    packages=['evaluator'],
    options={"bdist_wheel": {"universal": True}},
    url='https://github.com/philhanna/RPNCalculator',
    license='MIT',
    author='Phil Hanna',
    author_email='ph1204@gmail.com',
    description='Reverse Polish notation calculator',
)
