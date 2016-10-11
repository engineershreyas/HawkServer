Databases Crime Project Server
==============================
# By: Shreyas Hirday and Tanya Balaraju

## Instructions to run this server (Linux/ Mac OSX)

* It is recommened to setup a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in your directory
* Once that is setup and you are in your project directory do ". venv/bin/activate" in your terminal
* After that do "export FLASK_APP=app.py" in your terminal
* From then on, to run the server you can do "flask run" in your root directory in terminal and go to the returned URL in your browser to see the results

## Modules

### dbhelper.py

This module provides assistance (in a modular way) to execute sql commands to the DB.
Currently, the doOperation() function takes in a command, whether or not it is a retrieve command and how many results.

### spotcrime.py

This module is a python api for getting data from [SpotCrime](https://www.spotcrime.com).
We can pass in latitude, longitude, and a radius to get this data.
This is to be used to populate our personal database, not to show data to the client.

# IN PROGRESS
