'''
debug.py contains functions needed to analyze the thermocouple and RHT data from the Volatility and Polarity Separator (VAPS)
'''
import os
import glob
import re
import sys
import warnings
import pandas as pd
import matplotlib.pyplot as plt

from ..thermo.io import get_files, numericalSort

__all__ = ['read_data_vaps','VAPS_Debug']


def valid_row(ind):
    return True if (type(pd.to_datetime(ind)) is pd.tslib.Timestamp) else False

def clean_short_rows(data):
    '''
    Cleans up all short rows in time-indexed dataframe. Returns clean df
    '''
    data['tmp'] = data.index
    data['tmp'] = data['tmp'].apply(valid_row)
    data = data[data['tmp'] == True]
    del data['tmp']
    data.index = pd.to_datetime(data.index)

    return data


def read_data_vaps(runDir=os.getcwd(), sample_int='5S', start=None, end=None):
    '''
    Reads the vaps output files and imports data into beautiful dataframes for easy visualization.

    >>>data = read_data_vaps("C:/Users/David/Desktop/VAPS Data/")
    '''

    # Get the list of files
    files = get_files("Vaps", fileType='txt', runDir=runDir, start=start, end=end)

    data = pd.DataFrame()

    for each in files:
        newData = pd.read_table(each, sep='\t', header=0, parse_dates=True, index_col='Date/Time', error_bad_lines=True)
        data = pd.concat([data, newData])

    data = clean_short_rows(data)
    data = data.resample(sample_int)

    return data


class VAPS_Debug:
    '''
    Plot thermocouple data for the VAPS

    >>>vaps = VAPS_Debug(runDir)
    >>>vaps.plot_trap()

    '''

    def __init__(self, runDir, start=None, end=None, sample_int='5S'):
        self.runDir =runDir
        self.data = read_data_vaps(runDir, sample_int=sample_int, start=start, end=end)
        self.title = "VAPS Trap Thermocouple Data"
        self.xlabel = "Timestamp"
        self.ylabel = "Temperature (C)"

        # Eliminate all data where TC value is less than zero because that's just ridiculous
        self.data = self.data[self.data > 0]

    def plot_trap(self, args={}):
        '''
        Plots the thermocouple data for the VAPS Trap. dates must be in format to select from normal dataframe
        '''

        # Plot some shit!
        fig, ax = plt.subplots(1, figsize=(10,6))
        ax.set_title(self.title, fontsize=16)
        ax.set_xlabel(self.xlabel, fontsize=14)
        ax.set_ylabel(self.ylabel, fontsize=14)

        # Figure out what else I need to plot
        if len(args) == 0:
            sys.exit("There are no columns to plot! Please select some :)")

        for key, value in args.iteritems():
            try:
                if args[key].has_key('color'):
                    self.data[key].plot(color=value['color'], label=value['label'])
                else:
                    self.data[key].plot(label=value['label'])
            except:
                warnings.warn("Could not plot %s" % key)


        plt.legend(bbox_to_anchor=(1.10, 1), loc=2, borderaxespad=0.)


        plt.tight_layout()
        plt.show()

        return fig, ax