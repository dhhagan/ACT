"""
	Classes and functions used to visualize data for thermo scientific analyzers
"""
from pandas import Series, DataFrame
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import dates as d
import os
import math
import glob
import matplotlib
import warnings



def diurnal_plot(data, all_data=True, dates=[], shaded=False, title="Diurnal Profile of Trace Gases", xlabel="Local Time: East St. Louis, MO"):
    '''
       
	   If plotting the entire DataFrame (data), choose all_data=True, else choose all_data=False
	   and declare the date or dates to plot as a list.

       `data` should be a pandas core DataFrame with time index and each trace gas concentration as a column
       
       returns a single plot for NOx, SO2, and O3
    '''
    
    # Check to make sure the data is a valid dataframe
    if not isinstance(data, pd.DataFrame):
         print ("data is not a pandas DataFrame, thus this will not end well for you.")
         exit
    
    # Check to see if all_data = True and a date is defined
    if all_data == True and len(dates) != 0:
        warnings.warn("You have conflicting dates. Please choose either `all` OR set the dates, but not both. Default has been set to plot all dates.")
        
    # If not plotting all the data, truncate the dataframe to include only the needed data
    if all_data == False:
        # Check to see if dates is a list or a string
        if type(dates) == list:
            if len(dates) == 0:
                warnings.warn("all_dates has been set to False, but no dates have been declared.")
                exit
            elif len(dates) == 1:
                data = data[dates[0]]
            else:
                data = data[dates[0]:dates[1]]
        else:
            warnings.warn("dates is not properly configured")
            exit
      
    # Add columns for time to enable simple diurnal trends to be found
    data['Time'] = data.index.map(lambda x: x.strftime("%H:%M"))
    
    # Group the data by time and grab the statistics
    grouped = data.groupby('Time').describe().unstack()
    
    # set the index to be a str
    grouped.index = pd.to_datetime(grouped.index.astype(str))

    # Plot
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(10,9), sharex=True)

    # Set plot titles and labels
    ax1.set_title(title, fontsize=14)
    ax1.set_ylabel(r'$\ [NO_x]  (ppb)$', fontsize=14, weight='bold')
    ax2.set_ylabel(r'$\ [SO_2]  (ppb)$', fontsize=14)
    ax3.set_ylabel(r'$\ [O_3]  (ppb)$', fontsize=14)
    ax3.set_xlabel(xlabel, fontsize=14)

    # Make the ticks invisible on the first and second plots
    plt.setp( ax1.get_xticklabels(), visible=False)
    plt.setp( ax2.get_xticklabels(), visible=False)

    # Set y min to zero just in case:
    ax1.set_ylim(0,grouped['nox']['mean'].max()*1.05)
    ax2.set_ylim(0,grouped['so2']['mean'].max()*1.05)
    ax3.set_ylim(0,grouped['o3']['mean'].max()*1.05)

    # Plot means
    ax1.plot(grouped.index, grouped['nox']['mean'],'g', linewidth=2.0)
    ax2.plot(grouped.index, grouped['so2']['mean'], 'r', linewidth=2.0)
    ax3.plot(grouped.index, grouped['o3']['mean'], 'b', linewidth=2.0)
    
    # If shaded=true, plot trends
    if shaded == True:
        ax1.plot(grouped.index, grouped['nox']['75%'],'g')
        ax1.plot(grouped.index, grouped['nox']['25%'],'g')
        ax1.set_ylim(0,grouped['nox']['75%'].max()*1.05)
        ax1.fill_between(grouped.index, grouped['nox']['mean'], grouped['nox']['75%'], alpha=.5, facecolor='green')
        ax1.fill_between(grouped.index, grouped['nox']['mean'], grouped['nox']['25%'], alpha=.5, facecolor='green')
        
        ax2.plot(grouped.index, grouped['so2']['75%'],'r')
        ax2.plot(grouped.index, grouped['so2']['25%'],'r')
        ax2.set_ylim(0,grouped['so2']['75%'].max()*1.05)
        ax2.fill_between(grouped.index, grouped['so2']['mean'], grouped['so2']['75%'], alpha=.5, facecolor='red')
        ax2.fill_between(grouped.index, grouped['so2']['mean'], grouped['so2']['25%'], alpha=.5, facecolor='red')
        
        ax3.plot(grouped.index, grouped['o3']['75%'],'b')
        ax3.plot(grouped.index, grouped['o3']['25%'],'b')
        ax3.set_ylim(0,grouped['o3']['75%'].max()*1.05)
        ax3.fill_between(grouped.index, grouped['o3']['mean'], grouped['o3']['75%'], alpha=.5, facecolor='blue')
        ax3.fill_between(grouped.index, grouped['o3']['mean'], grouped['o3']['25%'], alpha=.5, facecolor='blue')
    
    # Get/Set xticks
    ticks = ax1.get_xticks()
    ax3.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 5))
    ax3.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 25), minor=True)
    ax3.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M %p'))

    # Make the layout tight to get rid of some whitespace
    plt.tight_layout()
    plt.show()
    
    return (fig, (ax1, ax2, ax3))
	
	
class Thermo():
    '''
        Allows for easy plotting of internal instrument data. Currently supports the 
        following models:
            - NO, NO2, NOx (42I)
            - O3 (49I)
            - SO2 (43I)
    '''
      
    def __init__(self, data):
        self.data = data
        
    def debug_plot_nox(self, args={}):
        '''
            Plots thermo scientific instrument data for debugging purposes. The top plot contains internal
			instrument data such as flow rates and temperatures. The bottom plot contains trace gas data for the
			instrument.
			
			Returns the figure and three axes objects for the plot
        '''
		#  Example for plotting debug plot
		# >>> nox = Thermo(data)
		# >>> f, (a1, a2, a3) = nox.debug_plot_nox()
      
        # Set default values for plot based on what is/isn't in the args dictionary
        default_args = {
            'title':"Debug Plot for " + r'$\ NO_{x} $' + ": Model 49I",
            'xlabel':'Local Time, East St Louis, MO',
            'ylabpressure':'Flow (LPM)',
            'ylabgas':'Gas Conc. (ppb)',
            'ylabtemp':'Temperature (C)',
            'color_no':'#FAB923',
            'color_nox':'#FC5603',
            'color_no2':'#FAE823',
            'title_fontsize':'18',
            'labels_fontsize':'14',
            'grid':False
            }
        
        for key, val in default_args.iteritems():
            if args.has_key(key):
                default_args[key] = args[key]
        
        # Set up Plot and all three axes
        fig, (ax1, ax3) = plt.subplots(2, figsize=(10,6), sharex=True)
        ax2 = ax1.twinx()
        
        # Set axes labels and titles
        ax1.set_title(default_args['title'], fontsize=default_args['title_fontsize'])
        ax1.set_ylabel(default_args['ylabpressure'], fontsize=default_args['labels_fontsize'])
        ax2.set_ylabel(default_args['ylabtemp'], fontsize=default_args['labels_fontsize'])
        ax3.set_ylabel(default_args['ylabgas'], fontsize=default_args['labels_fontsize'])
        ax3.set_xlabel(default_args['xlabel'], fontsize=default_args['labels_fontsize'])
        
        # Make the ticks invisible on the first and second plots
        plt.setp( ax1.get_xticklabels(), visible=False)
 
        # Plot the debug data on the top graph
        m = max(self.data.convt.max(),self.data.intt.max(),self.data.pmtt.max())
        self.data['convt'].plot(ax=ax2, label=r'$\ T_{converter}$')
        self.data['intt'].plot(ax=ax2, label=r'$\ T_{internal}$')
        self.data['rctt'].plot(ax=ax2, label=r'$\ T_{reactor}$')
        self.data['pmtt'].plot(ax=ax2, label=r'$\ T_{PMT}$')
        self.data['smplf'].plot(ax=ax1, label=r'$\ Q_{sample}$', style='--')
        self.data['ozonf'].plot(ax=ax1, label=r'$\ Q_{ozone}$', style='--')
        
        # Plot the gas data on the bottom graph
        self.data['no'].plot(ax=ax3, label=r'$\ NO $', color=default_args['color_no'])
        self.data['no2'].plot(ax=ax3, label=r'$\ NO_{2}$', color=default_args['color_no2'])
        self.data['nox'].plot(ax=ax3, label=r'$\ NO_{x}$', color=default_args['color_nox'], ylim=(0,math.ceil(self.data.nox.max()*1.05)))

        # Get labels for the top graph to build a single legend
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        plt.legend(lines+lines2,labels+labels2,bbox_to_anchor=(1.10,1), loc=2, borderaxespad=0.)
        ax3.legend(bbox_to_anchor=(1.10,1.), loc=2, borderaxespad=0.)  
        
        # Hide the grid lines
        ax1.grid(default_args['grid'])
        ax2.grid(default_args['grid'])
        ax3.grid(default_args['grid'])
        
        plt.tight_layout()
        plt.show() 
        
        return (fig, (ax1, ax2, ax3))
    
    def debug_plot_sox(self, args={}):
        '''
            Plots thermo scientific instrument data for debugging purposes. The top plot contains internal
			instrument data such as flow rates and temperatures. The bottom plot contains trace gas data for the
			instrument.
			
			Returns the figure and three axes objects for the plot
        '''
		#  Example for plotting debug plot
		# >>> nox = Thermo(data)
		# >>> f, (a1, a2, a3) = nox.debug_plot_nox()
      
        # Set default values for plot based on what is/isn't in the args dictionary
        default_args = {
            'title':"Debug Plot for " + r'$\ SO_{2} $' + ": Model 43I",
            'xlabel':'Local Time, East St Louis, MO',
            'ylabpressure':'Flow (LPM)',
            'ylabgas':'Gas Conc. (ppb)',
            'ylabtemp':'Temperature (C)',
            'color_so2':'green',
            'title_fontsize':'18',
            'labels_fontsize':'14',
            'grid':False
            }
        
        for key, val in default_args.iteritems():
            if args.has_key(key):
                default_args[key] = args[key]
        
        # Set up Plot and all three axes
        fig, (ax1, ax3) = plt.subplots(2, figsize=(10,6), sharex=True)
        ax2 = ax1.twinx()
        
        # Set axes labels and titles
        ax1.set_title(default_args['title'], fontsize=default_args['title_fontsize'])
        ax1.set_ylabel(default_args['ylabpressure'], fontsize=default_args['labels_fontsize'])
        ax2.set_ylabel(default_args['ylabtemp'], fontsize=default_args['labels_fontsize'])
        ax3.set_ylabel(default_args['ylabgas'], fontsize=default_args['labels_fontsize'])
        ax3.set_xlabel(default_args['xlabel'], fontsize=default_args['labels_fontsize'])
        
        
        # Make the ticks invisible on the first and second plots
        plt.setp( ax1.get_xticklabels(), visible=False)
 
        # Plot the debug data on the top graph
       # m = max(self.data.convt.max(),self.data.intt.max(),self.data.pmtt.max())
        self.data['intt'].plot(ax=ax2, label=r'$\ T_{internal}$')
        self.data['rctt'].plot(ax=ax2, label=r'$\ T_{reactor}$')
        
        self.data['smplfl'].plot(ax=ax1, label=r'$\ Q_{sample}$', style='--')
        
        # Plot the gas data on the bottom graph
        self.data['so2'].plot(ax=ax3, label=r'$\ SO_2 $', color=default_args['color_so2'], ylim=[0,self.data['so2'].max()*1.05])
        
        # Get labels for the top graph to build a single legend
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        plt.legend(lines+lines2,labels+labels2,bbox_to_anchor=(1.10,1), loc=2, borderaxespad=0.)
        ax3.legend(bbox_to_anchor=(1.10,1.), loc=2, borderaxespad=0.)  
        
        # Hide the grid lines
        ax1.grid(default_args['grid'])
        ax2.grid(default_args['grid'])
        ax3.grid(default_args['grid'])
        
        plt.tight_layout()
        plt.show() 
        
        return (fig, (ax1, ax2, ax3))
    
    def debug_plot_o3(self, args={}):
        '''
            Plots thermo scientific instrument data for debugging purposes. The top plot contains internal
			instrument data such as flow rates and temperatures. The bottom plot contains trace gas data for the
			instrument.
			
			Returns the figure and three axes objects for the plot
        '''
		#  Example for plotting debug plot
		# >>> nox = Thermo(data)
		# >>> f, (a1, a2, a3) = nox.debug_plot_nox()
      
        # Set default values for plot based on what is/isn't in the args dictionary
        # Set default values for plot based on what is/isn't in the args dictionary
        default_args = {
            'title':"Debug Plot for " + r'$\ O_{3} $' + ": Model 49I",
            'xlabel':'Local Time, East St Louis, MO',
            'ylabpressure':'Flow (LPM)',
            'ylabgas':'Gas Conc. (ppb)',
            'ylabtemp':'Temperature (C)',
            'color_o3':'blue',
            'title_fontsize':'18',
            'labels_fontsize':'14',
            'grid':False
            }
        
        for key, val in default_args.iteritems():
            if args.has_key(key):
                default_args[key] = args[key]
        
        # Set up Plot and all three axes
        fig, (ax1, ax3) = plt.subplots(2, figsize=(10,6), sharex=True)
        ax2 = ax1.twinx()
        
        # Set axes labels and titles
        ax1.set_title(default_args['title'], fontsize=default_args['title_fontsize'])
        ax1.set_ylabel(default_args['ylabpressure'], fontsize=default_args['labels_fontsize'])
        ax2.set_ylabel(default_args['ylabtemp'], fontsize=default_args['labels_fontsize'])
        ax3.set_ylabel(default_args['ylabgas'], fontsize=default_args['labels_fontsize'])
        ax3.set_xlabel(default_args['xlabel'], fontsize=default_args['labels_fontsize'])
        
        # Make the ticks invisible on the first and second plots
        plt.setp( ax1.get_xticklabels(), visible=False)
 
        # Plot the debug data on the top graph
       # m = max(self.data.convt.max(),self.data.intt.max(),self.data.pmtt.max())
        self.data['bncht'].plot(ax=ax2, label=r'$\ T_{bench}$')
        self.data['lmpt'].plot(ax=ax2, label=r'$\ T_{lamp}$')
        self.data['flowa'].plot(ax=ax1, label=r'$\ Q_{A}$', style='--')
        self.data['flowb'].plot(ax=ax1, label=r'$\ Q_{B}$', style='--')
        
        # Plot the gas data on the bottom graph
        self.data['o3'].plot(ax=ax3, label=r'$\ O_3 $', color=default_args['color_o3'], ylim=[0, self.data['o3'].max()*1.05])
        
        # Get labels for the top graph to build a single legend
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        plt.legend(lines+lines2,labels+labels2,bbox_to_anchor=(1.10,1), loc=2, borderaxespad=0.)
        ax3.legend(bbox_to_anchor=(1.10,1.), loc=2, borderaxespad=0.)  
        
        # Hide the grid lines
        ax1.grid(default_args['grid'])
        ax2.grid(default_args['grid'])
        ax3.grid(default_args['grid'])
        
        plt.tight_layout()
        plt.show() 
        
        return (fig, (ax1, ax2, ax3))
		
	