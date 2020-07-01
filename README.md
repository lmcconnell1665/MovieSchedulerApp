# MovieSchedulerApp

## Summary of project
This application starts by reading in data from the DataIn folder and creating a unique (and optimized) schedule for each theatre based on the unique parameters that are passed from the input files. These results are then displayed in a Gantt chart build using the Dash libraries.

## More details
When the application is first launched 'CreateSchedules.py' scans the DataIn directory to see if there are any new folders (one folder for each unique cinema). For any folder that doesn't have a corresponding schedule in the Schedules folder, the 'movieModel.py' function is called.

This function uses the pyomo solver to create an optimized schedule based on the parameters (number of auditoriums, size of auditoriums, required pre/post cleaning times, and expected demand, etc.) that are passed in from the Theatre_Bookings and Theatre_Details files in the DataIn directory.

Once all schedules are built, the created schedules are stored and the Gantt chart (built using Dash by Plot.ly) shows schedule details.

