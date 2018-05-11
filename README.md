# MapAnythingChallenge

## Remote Service Access Scripting Exercise

### Part 1:
A customer is interested in solving very large routing problems. One of the inputs needed for these problems is the travel time (and/or distance) matrix between all of the locations. Using the open source OSRM service, estimate how long it will take to produce these matrices for various #s of locations, and explore if there are any other factors that appear to influence the time required to get a matrix.

Along with the data and any findings, this exercise should be done in such a way that the work could be plugabble to an existing project as a module and also could be handed off to a co-worker upon completion. 

### Part 2:Beverage Salesperson Challenge Problem

The chicago_data_clean.csv file contains 8 columns that represent historical service by a beverage distributor in Chicago. The company wants a revised 5 day plan for its drivers (who are actually salespeople) to service these “outlets”. The following constraints apply:

* Each visit requires 20 minutes
* The working day is 8 hours long (9am to 5pm)
* The rightmost 5 columns represent a count of the # of historical visits on each weekday over a 13 week period. The outlets prefer to be visited on the same day - the day that they receive serviced most often over the previous 13 weeks. However, it is possible (but undesirable) to move the visit one day in either direction from this most common day (i.e. Wed can go to Tue or Thu, Fri can go to Thu or Mon).
* The distributor wants to use as few drivers as possible
* The routes should be “fair” across drivers
* The company has routed by hand historically and the routes should “look good”
* The workday starts at the first visit of the day and ends at the last visit of the day. The company doesn’t treat its drivers that well and so they do not account for the existing drivers’ home address
* Any info regarding the “extra cost” of hitting each outlet is valuable - they have their own internal estimates for the value of an outlet and maybe it isn’t worth it to even visit some of them
* Presenting a solution and describing what makes one solution “better” than another is an important part of the exercise, as is any feedback on the computational complexity of the problem.
