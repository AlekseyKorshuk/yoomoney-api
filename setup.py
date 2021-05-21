from setuptools import setup

setup(
    name='YooMoney',
    version='1.0.0',
    packages=['yoomoney', 'yoomoney.account', 'yoomoney.history', 'yoomoney.quickpay', 'yoomoney.authorize',
              'yoomoney.operation', 'yoomoney.operation_details'],
    url='https://github.com/AlekseyKorshuk/yoomoney-api',
    license='GPL-3.0',
    author='AlekseyKorshuk',
    author_email='t.me/goodimpression',
    description='Unofficial YooMoney API python library'
)
