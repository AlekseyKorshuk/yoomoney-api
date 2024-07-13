from setuptools import setup, find_packages, Extension

setup(
    name='YooMoney',
    version='0.1.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/AlekseyKorshuk/yoomoney-api',
    license='GPL-3.0',
    author='AlekseyKorshuk',
    author_email='ale-kor02@mail.ru',
    description='Unofficial YooMoney API python library',
    long_description=str(open('README.rst').read())
)
