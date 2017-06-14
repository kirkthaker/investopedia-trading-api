from setuptools import setup, find_packages 

setup(
  name = 'investopedia-trading-api',
  packages = ['investopedia-trading-api'],
  version = '1.0',
  description = 'An API for Investopedia\'s paper trading simulator',
  author = 'Kirk Thaker',
  author_email = 'kirkthaker66@gmail.com',
  url = 'https://github.com/kirkthaker/investopedia-trading-api',
  download_url = 'https://github.com/kirkthaker/investopedia-trading-api/tarball/0.1',
  keywords = ['trading', 'finance', 'investopedia', 'algorithmic'],
  classifiers = [],
  install_requires=['mechanicalsoup'],
)
