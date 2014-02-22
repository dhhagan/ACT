# /ACT/setup.py

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(name='ACT',
      version='0.0.6',
      description='Python library for analyzing trace gas data from thermo scientific gas analyzers',
      url='http://github.com/dhhagan/ACT',
      author='David H Hagan',
      author_email='david@davidhhagan.com',
      license='MIT',
	  keywords=['ACT', 'thermo scientific', 'atmospheric science'],
      packages=['ACT',
				'ACT.thermo',
				'ACT.pam',
				'ACT.vaps',
			],
	  install_requires=[
		'pandas',
		'numpy',
		'xlrd'
	  ],
      zip_safe=False)