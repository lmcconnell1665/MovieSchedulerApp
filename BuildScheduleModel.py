# Luke McConnell
# Created: 6/21/20
# Updated: 6/21/20
# Based off of movieModel.py

# Uses pyomo solver to create a schedule for a theatre

import pandas as pd
import datetime as dt
import numpy as np
from pyomo.environ import *

bookingDF = pd.read_csv("DataIn/Pinnacle_8" + "/Theatre_Bookings.csv")
detailsDF = pd.read_csv("DataIn/Pinnacle_8" + "/Theatre_Details.csv")
TUsize = 15
startTime = dt.datetime.strptime("06/21/20 13:00:00", '%m/%d/%y %H:%M:%S')
endTime = dt.datetime.strptime("06/21/20 22:45:00", '%m/%d/%y %H:%M:%S')

# creates numTh
numTh = detailsDF.shape[0]

# total minutes from earliest possible Show Time to Latest Possible. This will be used to form our grid.
totalMinutes = (endTime-startTime).total_seconds()/60

# number of time units needed.
numTU = np.floor(totalMinutes/TUsize) # flooring keeps everything within bounds.

# no one likes /, -, or spaces in column names. - is a special char.
bookingDF.columns = bookingDF.columns.str.replace('[/\- ]', '_')

# Cut the Dataframe to only keep what we are currently using.
# We will need to come back to this to include more features.
bookingDF['totalPostTime'] = bookingDF.Runtime + bookingDF.Post_Clean_Time
bookingDF['totalPreTime'] = bookingDF.Pre_Show_Advertising + bookingDF.Trailers
bookingDF = bookingDF.drop(columns = ['Playing', 'Format', "Auditorium_Size_Preference", "Expected_Demand"])

# Create model
model = ConcreteModel()

# Parameters...
movies = bookingDF.Print_Film
theatres = list(range(numTh))
timeUnits = list(range(int(numTU)))

# lesser params...
# Creates a dictionary of the number of time units need to show a movie by movie.
moviePostTimeUnits = {bookingDF.Print_Film[i]:ceil(bookingDF.totalPostTime[i]/TUsize) for i in range(len(movies))}
moviePreTimeUnits = {bookingDF.Print_Film[i]:ceil(bookingDF.totalPreTime[i]/TUsize) for i in range(len(movies))}
movieRunTimes = {bookingDF.Print_Film[i]:ceil(bookingDF.Runtime[i]/TUsize) for i in range(len(movies))}
movieTrailerTimes = {bookingDF.Print_Film[i]:ceil(bookingDF.Trailers[i]/TUsize) for i in range(len(movies))}
moviePreAdTimes = {bookingDF.Print_Film[i]:ceil(bookingDF.Pre_Show_Advertising[i]/TUsize) for i in range(len(movies))}
movieCleanUpTimes = {bookingDF.Print_Film[i]:ceil(bookingDF.Post_Clean_Time[i]/TUsize) for i in range(len(movies))}
 
# I want to index my minimum performance with movies... so... let's make a dictionary.
movieMinimumPerformanceCount = {bookingDF.Print_Film[i]:bookingDF.Minimum_Performance_Count[i] for i in range(len(movies))}

# Variable
model.startTimes = Var(movies, theatres, timeUnits, domain = Binary)
model.minMovieTimeDiff = Var(movies)

# Objective function
model.objectiveFun = Objective(
    expr = numTU*100*sum([model.startTimes[m,th,t] for m in movies for th in theatres for t in timeUnits]),
    sense = maximize)

# Constraints...
model.noTwoShows = ConstraintList()
for th in theatres:
    for t in timeUnits:
        model.noTwoShows.add(sum(
            [
                model.startTimes[m,th,lil_t] 
                for m in movies
                for lil_t in range(int(max(0,t+1-moviePostTimeUnits[m])), int(min(numTU,t+ moviePreTimeUnits[m])))

            ]) <=1)
