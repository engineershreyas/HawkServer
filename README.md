Databases Crime Project Server (a.k.a Hawk Server)
==================================================
# By: Shreyas Hirday and Tanya Balaraju

## Instructions to run this server (Linux/ Mac OSX)

* It is recommened to setup a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in your directory
* Once that is setup and you are in your project directory do ". venv/bin/activate" in your terminal
* After that do "export FLASK_APP=app.py" in your terminal
* From then on, to run the server you can do "flask run" in your root directory in terminal and go to the returned URL in your browser to see the results

## Modules

### dcapi.py
This module is the api for the Hawk app. It includes functions to register and login users, post reviews, update crimes data, and update gunlaws data. [app.py](https://github.com/HirDaysOfTheWeek/DatabasesCrimeServer/blob/master/app.py) directly interfaces with this module and all endpoints route requests to these functions.

### dbhelper.py

This module provides assistance (in a modular way) to execute sql commands to the DB.
Currently, the doOperation() function takes in a command, whether or not it is a retrieve command and how many results.

### spotcrime.py

This module is a python api for getting data from [SpotCrime](https://www.spotcrime.com).
We can pass in latitude, longitude, and a radius to get this data.
This is to be used to populate our personal database, not to show data to the client.

### gunlaws.py
This module has basic helper functions for returning abbreviations of all 50 states in the USA and a dictionary mapping those states to their gun law types, which can either be OC (Open Carry), CC (Concealed Carry), or NC (No Carry). Note that this data is generalized and is categorized based on state law and de facto law, actual data may vary for specific areas within a state.

# IN PROGRESS
