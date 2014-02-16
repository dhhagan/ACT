# /ACT/io/parse.py

def numericalSort(value):
	numbers = re.compile(r'(\d+)')
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts

	
def get_files(instrument=None, start=None, end=None, fileType=None, runDir=os.getcwd()):
    
    '''
        Grabs all files in runDir with filename including `instrument` and file extension `fileType`.
        The daterange can be set using `start` and `end`. `fileType` should not have the period included.
    '''
    
    if os.getcwd != runDir:
        os.chdir(runDir)
    
    try:
        files = glob.glob('*%s*.%s' % (instrument, fileType))
        if len(files) == 0:
            warnings.warn("There were no files found like '%s'" % (instrument))
    except:
        sys.exit("No files were found with file name like: %s" % (instrument))
        
    # Sort the files by date in reverse order
    files = sorted(files, key=numericalSort, reverse=False)
    
    filesinrange = []
    
    if (start == None and end == None): # if end/start are not defined
        filesinrange = files
    elif (start != None and end == None):
        for each in files:
            try:
                if pd.to_datetime(each.split(' ')[1], format='%m%d%y') >= pd.to_datetime(start):
                    filesinrange.append(each)
            except:
                pass
            
    elif (start != None and end != None):
        for each in files:
            try:
                filedate = pd.to_datetime(each.split(' ')[1], format='%m%d%y')
                if filedate >= pd.to_datetime(start) and filedate <= pd.to_datetime(end):
                    filesinrange.append(each)
            except:
                pass
            
    return filesinrange
	
	
	
def read_thermo_dat(model='nox', runDir=os.getcwd(), sample_int='1min', start=None, end=None):
    '''
        Reads thermo data from .dat file type.
        model = one of: nox, sox, or o3
        returns the number of files read and DataSeries containing all data munged and organized for the user for the 
            Thermo Scientific line of atmospheric gas analyzers
    '''
    
    # If the data is in a different directory, change the directory
    if os.getcwd() != runDir:
        os.chdir(runDir)
    
    # Set the model name based on input
    if model =='nox':
        instrument = '42I'
    elif model == 'sox':
        instrument = '43I'
    elif model == 'o3':
        instrument = '49I'
    else:
        sys.exit("The model you defined is not valid or supported yet.")
    
    # grab all files in the directory for a given instrument with the .dat file extension
    files = get_files(instrument,fileType='dat',start=start, end=end, runDir=runDir)
    
    fileNo = 1
    data = DataFrame()
    
    # Concatenate the data from each file together to build one big dataframe
    for each in files:
        newData = pd.read_table(each, sep='\s+', skiprows=4, header=5, parse_dates=[[1,0]], keep_date_col=True, index_col='Date_Time', warn_bad_lines=True)
        data = pd.concat([data, newData])
        fileNo += 1
      
    # Create a duplicate column containing the index to easily drop all duplicate rows from merging files containing
    #  the same data
    data['stamp'] = data.index
    data = data.drop_duplicates(cols='stamp')
    
    # Depending on the model, do some stuff to clean it up
    if model == 'nox':
        data['no2'] = data['nox'] - data['no']
        
    # resample the data based on chosen imput
    data = data.resample(sample_int)
    
    return (fileNo, data)
	
	
def read_thermo_xlsx(filename=None, sheetname='Sheet1', runDir=os.getcwd(), sample_int='1min', skiprows=1):
    '''
        Reads thermo data from .xlsx file type.
        returns DataFrame containing all data munged and organized for the user for the 
            Thermo Scientific line of atmospheric gas analyzers
        This assumes all necessary data is in one sheet within one workbook.
    '''
    
    # If the data is in a different directory, change the directory
    if os.getcwd() != runDir:
        os.chdir(runDir)
        
    
    data = pd.read_excel(filename,sheetname, skiprows=skiprows, index_col=0)
      
    # Create a duplicate column containing the index to easily drop all duplicate rows from merging files containing
    #  the same data
    data['stamp'] = data.index
    data = data.drop_duplicates(cols='stamp')
     
    # resample the data based on chosen imput
    data = data.resample(sample_int)
    
    return data
	
	
def read_thermo_csv(filename=None, runDir=os.getcwd(), sample_int='1min'):
    '''
        Reads thermo data from .csv file type.
        returns DataFrame containing all data munged and organized for the user for the 
            Thermo Scientific line of atmospheric gas analyzers
        This assumes all necessary data is in one sheet within one workbook.
    '''
    
    # If the data is in a different directory, change the directory
    if os.getcwd() != runDir:
        os.chdir(runDir)
        
    
    data = pd.read_csv(filename, header=0, index_col=0, parse_dates=True, error_bad_lines=False)
      
    # Create a duplicate column containing the index to easily drop all duplicate rows from merging files containing
    #  the same data
    data['stamp'] = data.index
    data = data.drop_duplicates(cols='stamp')
     
    # resample the data based on chosen imput
    data = data.resample(sample_int)
    
    return data