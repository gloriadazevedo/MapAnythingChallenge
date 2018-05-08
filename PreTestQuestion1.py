import sys
import csv
import json
import urllib.request

def list_solution(lat_long_data):
	#need to loop through for each permutation of two locations
	#assume that there is the same distance going there and back so only need to calculate
	# the lower half of the matrix or n*(n-1) distances
	distance_matrix=[]
	for i in range(0,len(lat_long_data)-1):
		row_i=[]
		for ii in range(1,len(lat_long_data)):
			lat_1 = lat_long_data[i][0]
			long_1 = lat_long_data[i][1]
			lat_2 = lat_long_data[ii][0]
			long_2 = lat_long_data[ii][1]
			
			#send the request to the url to return a json
			req = urllib.request.Request('http://router.project-osrm.org/route/v1/driving/'+lat_1+','+long_1+';'+lat_2+','+long_2+'?overview=false')
			
			#parse the resulting JSON data
			with urllib.request.urlopen(req) as response:
				result = json.loads(response.read().decode('utf-8'))
				#since there are only 2 locations for each call, then the correct location pairs
				# are always the 0th or first result
				row_i.append(result['routes'][0]['distance'])
		
		#once we have all i-1 points, append the whole row
		distance_matrix.append(row_i)
		
	return distance_matrix
	
	#----------------------------------------------------
def dictionary_solution_v1(lat_long_data):
	#need to loop through for each permutation of two locations
	#assume that there is the same distance going there and back so only need to calculate
	# the lower half of the matrix or n*(n-1) distances
	
	#assume that there's a standard way of denoting the location order
	distance_dictionary={}
	for i in range(0,len(lat_long_data)-1):
		for ii in range(1,len(lat_long_data)):
			lat_1 = lat_long_data[i][0]
			long_1 = lat_long_data[i][1]
			lat_2 = lat_long_data[ii][0]
			long_2 = lat_long_data[ii][1]
			
			#send the request to the url to return a json
			req = urllib.request.Request('http://router.project-osrm.org/route/v1/driving/'+lat_1+','+long_1+';'+lat_2+','+long_2+'?overview=false')
			
			#get the JSON result and parse it
			with urllib.request.urlopen(req) as response:
				result = json.loads(response.read().decode('utf-8'))
				
				#make the key for the dictionary
				hash_key=lat_1+','+long_1,lat_2+','+long_2
				
				#check if there are duplicates and if not then add the key to the dictionary
				#since there are only 2 locations for each call, then the correct location pairs
				# are always the 0th or first result
				if hash_key not in distance_dictionary.keys():
					distance_dictionary[hash_key]=result['routes'][0]['distance']
				else: 
					print('Error! There are duplicates')
					break
		
	return distance_dictionary

	#----------------------------------------------------
def dictionary_solution_v2(lat_long_data):
	#need to loop through for each permutation of two locations
	#assume that there is the same distance going there and back so only need to calculate
	# the lower half of the matrix or n*(n-1) distances
	
	#assume that there's a standard way of denoting the location order
	distance_dictionary={}
	for i in range(0,len(lat_long_data)-1):
		for ii in range(1,len(lat_long_data)):
			lat_1 = lat_long_data[i][0]
			long_1 = lat_long_data[i][1]
			lat_2 = lat_long_data[ii][0]
			long_2 = lat_long_data[ii][1]
			
			#send the request to the url to return a json
			req = urllib.request.Request('http://router.project-osrm.org/route/v1/driving/'+lat_1+','+long_1+';'+lat_2+','+long_2+'?overview=false')
			
			#get the resulting JSON export
			with urllib.request.urlopen(req) as response:
				result = json.loads(response.read().decode('utf-8'))
				
				#make two keys so that they're not order dependent
				hash_key_1=lat_1+','+long_1,lat_2+','+long_2
				hash_key_2=lat_2+','+long_2,lat_1+','+long_1
				
				#check if there are duplicates and if not then add the key to the dictionary
				if hash_key_1 not in distance_dictionary.keys():
					distance_dictionary[hash_key_1]=result['routes'][0]['distance']
				else: 
					print('Error! There are duplicates')
					break
				
				#check if there are duplicates and if not then add the key to the dictionary
				#since there are only 2 locations for each call, then the correct location pairs
				# are always the 0th or first result
				if hash_key_2 not in distance_dictionary.keys():
					distance_dictionary[hash_key_2]=result['routes'][0]['distance']
				else: 
					print('Error! There are duplicates')
					break
		
	return distance_dictionary
	

def main(data_filename,header=False):
	#import list of lat-longs
	#expecting a list of lat-longs, comma separated 
	#2 floating numbers per line which would denote one location
	lat_long_import = []
	lat_long_header = []
	with open(data_filename, encoding='utf-8') as f:
			reader = csv.reader(f, skipinitialspace=True, quoting=csv.QUOTE_NONE)
			if header==True:
				#trying to get the header row in its own list
				lat_long_header=next(reader)
				next(reader) # skip header
			
			try:
				for row in reader:
					#append the row into the list as a tuple
					lat_long_import.append(tuple(row))

			except csv.Error as e:
				sys.exit('file {}, line {}: {}'.format(data_filename, reader.line_num, e))
	
	#remove duplicate locations from bad data
	lat_long_data = list(set(lat_long_import))
	
	#first solution using list indices
	print(list_solution(lat_long_data))
	
	#second solution using previously defined way of key definition
	print(dictionary_solution_v1(lat_long_data))
	
	#third solution of adding both ways to denote distance between two points to the dictionary
	print(dictionary_solution_v2(lat_long_data))
	
	
main('Data_set_small.csv',False)
	
#Notes and context
	#note that we actually get something like this for n = 7.
	# @@@@@@
	# @@@@@
	# @@@@
	# @@@
	# @@
	# @
	
	# but we really want something like (diagonals would be 0 for distance to the same point)
	# 0@@@@@@
	#  0@@@@@
	#   0@@@@
	#    0@@@
	#     0@@
	#      0@
	# 		0
	
	# to access the distance between locations i and j:
	#distance(i,j) = distance(j,i) = distance (min(i,j),max(i,j))
	#			   = distance_matrix[i][(j-1)-i]
	
	#Test: Want the distance between i = 1 and j = 3 for n = 7 (denoted by the x)
	# 0@@@@@@
	#  0@x@@@
	#   0@@@@
	#    0@@@
	#     0@@
	#      0@
	# 		0
	
	#Plugging into the formula we get distance_matrix[1][3-1-1] = distance_matrix[1][1]
	# @@@@@@
	# @x@@@
	# @@@@
	# @@@
	# @@
	# @
	
	#Test: Want the distance between i = 2 and j = 5 for n = 7 (denoted by the x)
	# 0@@@@@@
	#  0@@@@@
	#   0@@x@
	#    0@@@
	#     0@@
	#      0@
	# 		0
	
	#Plugging into the formula we get distance_matrix[2][5-1-2] = distance_matrix[2][2]
	# @@@@@@
	# @@@@@
	# @@x@
	# @@@
	# @@
	# @
	
#Another solution would be to populate a lookup table with each location pair as a key
# and the value would be the distance between them
	#This solution wouldn't require an ordered list to lookup in the specific matrix
	# but would require some sort of ordering of the location pair if there was only
	# one distinct key that would be made.
	
	#For example, if we wanted to find the distance between locations A and B
	# then we would need the indicies of A and B to find them in the list
	#However, if we knew that we could find it as distance_dictionary[[A,B]] then 
	# that would be more readable to code and extract the value.
	#To keep it as n*(n-1) calculations, then we would need to know a deterministic way
	# of writing the key--do we use [A,B] or [B,A]?
	#If we add both keys to the matrix then we still can compute the n*(n-1) distances
	# but would require more storage for 2*n*(n-1) keys.