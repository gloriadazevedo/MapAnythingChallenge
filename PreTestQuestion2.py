##Looking at the Chicago set
##First we need to check for each location, which weekday is most preferred

##Theoretically we may be able to do some clustering algorithm ahead of time
## to segment these locations into clusters and potentially assign drivers there so
## there isn't significant time lost to drive between far places
## In addition, breaking up the huge set of locations into smaller sets may require
## more drivers but the optimization would be easier on smaller set of locations

#import the data
data_filename = 'chicago_data_clean.csv'

chicago_data = []
chicago_data_header = []

with open(data_filename, encoding='utf-8') as f:
	reader = csv.reader(f, skipinitialspace=True, quoting=csv.QUOTE_NONE)
	if header==True:
		#trying to get the header row in its own list
		chicago_data_header=next(reader)
		next(reader) # skip header
	
	try:
		for row in reader:
			#append the row into the list as a tuple
			chicago_data.append(tuple(row))

	except csv.Error as e:
		sys.exit('file {}, line {}: {}'.format(data_filename, reader.line_num, e))
		

#make a lookup table for the preferred weekday (Monday = 1, Tuesday = 2...)
pref_weekday = {}

for i in range(0,len(chicago_data)):
	#find the max of the weekdays
	max_weekday = max(chicago_data[i][3:8])
	weekday_val = chicago_data[i][3:8].index(max_weekday) + 1 #monday is 1
	
	#add to location key
	pref_weekday[chicago_data[i][0]]=weekday_val
	
#for now assume that we can allocate drivers by day so 
#just create a baseline per day of demand
min_in_day = 8*60 #minutes
time_per_transaction = 20 #minutes
