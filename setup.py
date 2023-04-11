import os

from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='brbanks2ynab',
    version='0.0.2',
    url='https://github.com/andreroggeri/br-to-ynab',
    author='André Roggeri Campos',
    author_email='a.roggeri.c@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pynubank', 'ynab_sdk', 'inquirer', 'pyitau'
        # 'pybradesco@git+ssh://git@github.com/andreroggeri/pybradesco@2ac4a2b6037714872777091af5cc8ab952b121ff#egg=pybradesco',
        # 'python-alelo@git+ssh://git@github.com/andreroggeri/python-alelo@2ac4a2b6037714872777091af5cc8ab952b121ff#egg=python-alelo',
    ],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'brbanks2ynab = brbanks2ynab.cli:main'
        ]
    },
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
