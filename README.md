Databases Crime Project Server
==============================
# By: Shreyas Hirday and Tanya Balaraju

##Modules

### dbhelper.py

This module provides assistance (in a modular way) to execute sql commands to the DB.
Currently, the doOperation() function takes in a command, whether or not it is a retrieve command and how many results.

### spotcrime.py

This module is a python api for getting data from [SpotCrime](https://www.spotcrime.com).
We can pass in latitude, longitude, and a radius to get this data.
This is to be used to populate our personal database, not to show data to the client.
