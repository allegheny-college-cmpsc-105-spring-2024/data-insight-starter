#%% import statement

import numpy as np
import matplotlib.pyplot as plt

#%% function to recode categorical variables into numbers

# TODO: if your observations have categorical variables you want coded into
# numbers, update the strings and update the return numbers below

def format_sample(sample: str):
    """Reformat text to numbers."""
    try:
        return float(sample)
    except:
        if sample == 'Level 1': # <---TODO: update string if needed
            return 0 # <---------------TODO: udpate coded number if needed
        elif sample =='Level 2': # <---TODO: update string if needed
            return 1 # <---------------TODO: udpate coded number if needed
        elif sample =='Level 3': # <---TODO: update string if needed
            return 2 # <---------------TODO: udpate coded number if needed
        elif sample =='Level 4': # <---TODO: update string if needed
            return 3 # <---------------TODO: udpate coded number if needed
        elif sample =='five': # <---TODO: update string if needed
            return 3 # <---------------TODO: udpate coded number if needed
        return None
        
#%% read in the data into a numpy array

# TODO: check that the working directory is the data-insight directory by typing pwd
datafile = './assets/data/example.csv'
header = True

datamat = np.array([]) # this will hold data in a matrix
variables = np.array([]) # this will hold the header row

# read in the data and format into numbers
datalines = open(datafile, newline='\n').readlines()
for line in datalines:
  split_line = line.rstrip().split(',')
  if header:
    variables = np.append(variables,np.array(split_line))
    header = False
  else:
    datamat = np.append(datamat, np.array([format_sample(sample) for sample in split_line]))

if len(variables) == 0:
    variables = np.append(variables,np.array(split_line))
    

ncols = len(variables)
nrows = int(len(datamat)/ncols)
   
datamat = np.resize(datamat, (nrows,ncols))


#%% turn headers into variables names for indexing

# TODO: update the lines below to match the header names in your csv file
# TODO: ensure that none of the header names have spaces
# TODO: ensure that there are there are no extra names listed, only list those that are in the csv file
[
 col_1,
 col_2,
 col_3,
 col_4,
 col_5
] = np.arange(variables.size)



#%% group and/or filter variables with logical indexing

# TODO: following the example below, use one column to split up another column 

# find all rows in col_1 that have values > 50
good_rows = datamat[:,col_1] >  50
bad_rows = np.logical_not(good_rows)

# for the rows ^, read into a different column
good_obs = datamat[good_rows, col_2]
bad_obs = datamat[bad_rows, col_2]

#%% explore data so far

plt.subplots()
plt.pie([good_obs.size, bad_obs.size], labels = ['good', 'bad'])
plt.title("Count of Good vs Bad in col_2")

plt.subplots()
plt.bar([1,2], [np.mean(good_obs), np.mean(bad_obs)], tick_label = ['good', 'bad'])
plt.ylabel('mean')
plt.title("Mean of Good vs Bad in col_2")

plt.subplots()
plt.scatter(datamat[good_rows, col_2], datamat[good_rows, col_1])
plt.scatter(datamat[bad_rows, col_2], datamat[bad_rows, col_1])
plt.legend(('good', 'bad'))
plt.xlabel('col_2 units')
plt.ylabel('col_1 units')
plt.title('col_1 vs col_2')

plt.subplots()
plt.hist(datamat[:,col_2], bins = 4)
plt.hist(datamat[:,col_1], bins = 4)
plt.legend(('col_2', 'col_1'))
plt.xlabel('data value range')
plt.ylabel('count of values')
plt.title('distributions of col_1 and col_2')

#%% sample stats for good

# rename for convenience
x = datamat[good_rows, col_2]
y = datamat[good_rows, col_1]

xerror = x - np.mean(x)
yerror = y - np.mean(y)
sd_x = np.std(x) # standard dev. x
sd_y = np.std(y) # standard dev. y
n = np.size(x) # num observations

# correlation
r = np.sum(xerror*yerror) / ((n-1)*sd_x*sd_y)

# compute slope of a line; recall line formula = mx + b

m = r*sd_y/sd_x
b = np.mean(y) - m*np.mean(x)
line_fit_good = m*datamat[:, col_2] + b

#%% sample stats for bad

# bad form for software, gets the job done for data

# rename for convenience
xbad = datamat[bad_rows, col_2]
ybad = datamat[bad_rows, col_1]


xerrorbad = xbad - np.mean(xbad)
yerrorbad = ybad - np.mean(ybad)
sd_xbad = np.std(xbad) # standard dev. x
sd_ybad = np.std(ybad) # standard dev. y
nbad = np.size(xbad) # num observations

# correlation
rbad = np.sum(xerrorbad*yerrorbad) / ((nbad-1)*sd_xbad*sd_ybad)

# compute slope of a line; recall line formula = mx + b

mbad = rbad*sd_ybad/sd_xbad
bbad = np.mean(ybad) - mbad*np.mean(xbad)
line_fit_bad = mbad*datamat[:, col_2] + bbad

#%% make figure with stats

plt.subplots()
plt.scatter(x, y)
plt.plot(datamat[:, col_2], line_fit_good)
plt.scatter(xbad, ybad)
plt.plot(datamat[:, col_2], line_fit_bad)
plt.legend(('good', 'linear regression line good', 'bad', 'linear regression line bad'))
plt.xlabel('col_2 units')
plt.ylabel('col_1 units')
plt.title('col_1 vs col_2')

plt.subplots()
plt.bar([1,2], [m, mbad], tick_label = ['good', 'bad'])
plt.ylabel('slopes of regression lines')
plt.title('Rate of change of Good vs Bad')