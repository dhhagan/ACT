ACT
===

Python scripts for data analysis related to the Atmospheric Chemistry and Technology Lab

## What is it

<strong>ACT</strong> is a python library used to parse and analyze data relevant to the field of <strong>atmospheric chemistry.</strong>


## Main Features

1. Parse data from <strong>Thermo Scientific</strong> analyzers and export to csv, txt, or xlsx format
2. Import data from csv, xlsx, or txt files into pandas dataframes for further analysis
3. Plot <strong>diurnal profiles</strong> of trace gases
4. Parse and mesh data from <strong>Potential Aerosol Mass (PAM)</strong> LabVIEW program
5. Parse and plot data from <strong>Volatility and Polarity Separator (VAPS)</strong>

## Where to get it

The source code is currently hosted on GitHub at: http://github.com/dhhagan/ACT

## Dependencies

1. [**pandas**][pandas]
2. [**numpy**][numpy]
3. [**xlrd**][xlrd]


[numpy]: https://pypi.python.org/pypi/numpy
[pandas]: http://github.com/pydata/pandas
[xlrd]: https://pypi.python.org/pypi/xlrd

## Installation from sources

To install from the source, change your directory to directory where ACT is located and run:

    python setup.py install
    
    
## License

MIT

## Documentation

All documentation can be found on the [**ACT wiki**][ACT-wiki]

Ipython examples are available for the following:

1. [**Using the ACT Library for VAPS Analysis**][VAPS-ipython]
2. [**Using the ACT Python Library**][ACT-ipython]

[ACT-wiki]: https://github.com/dhhagan/ACT/wiki
[VAPS-ipython]: http://nbviewer.ipython.org/github/dhhagan/ACT/blob/master/IPython%20Notebooks%20and%20Tutorials/Using%20the%20ACT%20Library%20for%20VAPS.ipynb?create=1
[ACT-ipython]: http://nbviewer.ipython.org/url/davidhhagan.com/images/downloads/Plotting%20Trace%20Gas%20Data.ipynb?create=1

## Background

I started to develop this library because I was tired of dealing with Thermo Scientifics terrible data storage and don't like using software I have to pay for (Matlab, Igor Pro)

## Discussion and development

If you want to help develop this library, go for it. I can be reached at <strong>david@davidhhagan.com</strong>
