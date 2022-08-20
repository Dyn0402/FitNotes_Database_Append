# FitNotes_Database_Append
Append to FitNotes SQL database given csv in format of app's csv export. 
Each csv row must contain Exercise name which is matched to an ID in the SQL exercise table. 
The Exercise will need to be added manually through app before making backup if it doens't already exist.
Exercise Catergory column in csv ignored. Date, weight, and reps columns pulled and transformed to format expected by sql.
Comments will be pulled and appended to sql comments table. Dates will be registered but all times will be set to 2PM.

To run, make a backup .fitnotes file from the app (Settings->Backup). In addition, make a .csv file (Settings->Spreadsheet Export) to get the formatting.
Download both of these files and append personal exercises to the .csv (algorithm for doing so depends on format of personal exercise data, my impelementation not included).
In main.py, edit paths to sql database and csv file to these two files. Execute script and data from the csv will be appended to .fitnotes file.

Once .fitnotes restore file is updated via the script, import this file to the app (Settings->Import). 
Note that this will overwrite all current app data, so good idea to make/keep a clean backup in case.
