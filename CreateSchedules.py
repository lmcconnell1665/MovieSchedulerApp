# Luke McConnell
# This script creates the schedules for each theatre

import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import os
import re
import movieModel

def CheckSchedules():
    """Checks to see if a schedule exists and calls movieModel function if a schedule doesn't exist."""
    
    #Finds all of the sub-folders in the DataIn folder
    cinemaSFP = [f for f in os.scandir("DataIn") if (f.is_dir() & (f.name != ".ipynb_checkpoints"))]

    #Grabs all of the csv files in the schedules folder
    oldSchedules = [f.name for f in os.scandir("Schedules") if f.is_file() & bool(re.search(".*\.csv$",f.name))]

    #Checks to see if there is already a schedule made for each sub-folder in DataIn, if not, creates one
    for f in cinemaSFP:
        if f.name + "_Schedules.csv" not in oldSchedules:
            theatreBookingDF = pd.read_csv(f.path + "/Theatre_Bookings.csv")
            theatreDetailsDF = pd.read_csv(f.path + "/Theatre_Details.csv")
            movieModel.GenerateSchedule(theatreBookingDF, theatreDetailsDF).to_csv("Schedules/"+f.name+"_Schedules.csv", index=False)

    return None

if __name__ == "__main__":
    CheckSchedules()
        