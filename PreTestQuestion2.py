import sys
import csv
import json
import urllib.request
import math

#used for hierarchical clustering portion
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

#This function takes in a list of keys and the corresponding dictionary of 
#their lat long coordinates to compute a path between them of shortest distance
def determine_location_order(location_list,lookup_dict):
	#The lookup_dict should have possible values from the location_list as the key
	#then the information like distance calculation as the values.
	
	#I'm not sure how to reaccess the cluster information to start with the lowest
	#leaf then the next nearest location etc but I would do that here if possible
	#if the locations were submitted in order then we would actually not need the function
	#but otherwise we would need information from the cluster as well as the list
	
	#Another alternative is to brute force all permutations of the location_list
	#but that is computationally expensive
	

def main(data_filename,header==True)

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
	#key is the location id and the value is the day of week they prefer
	pref_weekday = {}

	#also add a dictionary to get a list of the location ids for each day of week
	#taking the length of this list would yield the number of stops required per weekday
	weekday_demand = {}

	#While iterating through we also create a dictionary with the location_id as a key again
	#but also hold their latitude and longitudes as a tuple or list
	lat_long_lookup = {}

	for i in range(0,len(chicago_data)):
		location_id = chicago_data[i][0]
		
		#find the max of the weekdays
		max_weekday = max(chicago_data[i][3:])
		#if there are ties, the index function will yield the index of the first occurrence
		weekday_val = chicago_data[i][3:8].index(max_weekday) + 1 #monday is 1
		
		#add to location key
		pref_weekday[location_id]=weekday_val
		
		#add to dictionary to look up latitudes and longitudes
		lat_long_lookup[location_id]=chicago_data[i][1:3]
		
		#add to weekday set of locations
		if weekday_val not in weekday_demand.keys():
			weekday_demand[weekday_val]=[location_id]
		else:
			weekday_demand[weekday_val].append(location_id)
		
	#for now assume that we can allocate drivers by day so 
	#just create a baseline per day of demand
	min_in_day = 8*60 #minutes
	time_per_transaction = 20 #minutes

	#print the resulting demand by weekday to verify all locations are covered
	#print(weekday_demand)

	#for each weekday, we need to create the adjacency matrix for the set of locations
	#then we find the minimum and maximum time to travel the distance between any
	# two locations in the set
	#The number of locations and the maximum distance between two locations will 
	#allow us to calculate an upper bound on the number of salespeople we need to service
	#all those locations on one day

	#create the list called master_schedule that is of the format
	#later on we define n to be the maximum number of jobs that a person can perform 
	#in one day
	#[[day,[location_1,location_2,...,location_n]],
	#[day,[location_11,location_12,....,location_1n]],...]
	master_schedule = []

	for day in weekday_demand.keys():
		#call the list of locations something so that it's easier
		location_id_set = weekday_demand[day]
		
		#Set the Maximum time to 0 so that we keep track of it
		max_time = 0
		
		#Also keep track of the minimum because why not.
		#Arbitrarily set it to be very high at the start so that we can decrease
		min_time = math.inf
		
		#adapt the code from Question 1
		for i in range(0,len(location_id_set)-1):
			#give it a variable name
			first_point = location_id_set[i]
			
			#Pull the latitude and longitude from the location lookup file
			lat_1 = lat_long_lookup[first_point][0]
			long_1 = lat_long_lookup[first_point][1]
			
			for ii in range(1,len(location_id_set)):
				second_point = location_id_set[ii]
				
				#Pull the latitude and longitude from the location lookup file
				lat_2 = lat_long_lookup[second_point][0]
				long_2 = lat_long_lookup[second_point][1]
				
				#Input the location variables into the pull 
				#At time of writing, this request would keep timing out so haven't tested the code yet
				req = urllib.request.Request('http://router.project-osrm.org/route/v1/driving/'+str(lat_1)+','+str(long_1)+';'+str(lat_2)+','+str(long_2)+'?overview=false')
				
				#print('http://router.project-osrm.org/route/v1/driving/'+lat_1+','+long_1+';'+lat_2+','+long_2+'?overview=false')
				
				#Extract the time (duration) instead of distance (returns in seconds)
				with urllib.request.urlopen(req) as response:
					result = json.loads(response.read().decode('utf-8'))
					result_time = result['routes'][0]['duration']/60.0
					
					#check if it's higher than the max; if so then reset the max
					if result_time>max_time:
						max_time = result_time
					
					#check if it's lower than the current min; if so, then reset the min
					if result_time<min_time:
						min_time = result_time
						
		#once we have the max time, we can calculate the maximum number of jobs that one person can go to in a day
		n=math.ceil((min_in_day+max_time)/(time_per_transaction+max_time))
		
		#then when we have the number of jobs, we can determine the requirements of people per day
		m = math.ceil(1.0*length(location_id_set)/n)
				
		#############################################
		#####NOTE: ALL THIS CODE BELOW IS UNTESTED###
		#############################################
				
		#Create a data matrix to implement hierarchical clustering
		#First iterate through all the locations in the list and then add their latitudes and longitudes
		lat_long_list = []
		for i in range(0,len(location_id_set)):
			#rename the location id 
			location_id_to_add = location_id_set[i]
			
			#grab the lat long pair
			lat_long_list.append(lat_long_lookup[location_id_to_add])
			
		#Create the linkage matrix
		#Not sure how to put a custom distance function in here.
		#Ideally the function would retrieve the duration or driving distance 
		#when calculating "closest" location in the linkage matrix but 
		#we can approximate for now with the euclidean distance just to get
		#relative closeness of locations
		Z = linkage(lat_long_list, 'euclidean')

		#retrieve the correct number of clusters for the number of salespeople, n
		#This should return an array of the same length as the lat_long_list
		#with integers corresponding to the cluster that the index was assigned to
		cluster_assignment = fcluster(Z, n, criterion='maxclust')
		
		#Initialize dictionary to assign locations to the salespeople
		cluster_dict = {}
		for i in range(0,len(cluster_assignment)):
			#check if the cluster is defined
			if cluster_assignment[i] not in cluster_dict.keys():
				#if not in the keys already then add it and create a list of location ids 
				#since we can access the array from the lat_long_list
				cluster_dict[cluster_assignment[i]]=[location_id_set[i]]
			else: 
				cluster_dict[cluster_assignment[i]].append(location_id_set[i])
			
		#Call another function to determine the order of schedules for each person
		for key in cluster_dict.keys():
			schedule_order = determine_location_order(cluster_dict[key],lat_long_lookup)
			master_schedule.append([day,schedule_order])
		
	return master_schedule
			
main('chicago_data_clean.csv',True)