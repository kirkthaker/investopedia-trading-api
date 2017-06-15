from setuptools import setup, find_packages

setup(
  name = 'InvestopediaApi',
  packages = ['InvestopediaApi'],
  version = '1.1',
  description = 'An API for Investopedia\'s paper trading simulator',
  author = 'Kirk Thaker',
  author_email = 'kirkthaker66@gmail.com',
  url = 'https://github.com/kirkthaker/investopedia-trading-api',
  download_url = 'https://github.com/kirkthaker/investopedia-trading-api/archive/1.1.tar.gz',
  keywords = ['trading', 'finance', 'investopedia', 'algorithmic'],
  classifiers = [],
  install_requires=['mechanicalsoup'],
)
