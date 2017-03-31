# snowBridge

This is an application written in Python.

Installation:
git clone https://github.com/xod442/imcServiceNow2.git

Change directory to the imcServiceNow2 folder
look at the requirements.txt file and verify you have the necessary
python libraries installed.


pip install -r requirements.txt (must have pip installed, if not:
sudo apt-get install python-pip

Start the application by issuing : python view.py

This application is currently non graphical. At this time you
must edit the views.py file and add you own credentials manually.

Sorry, working on making it pretty.....

Lokk for these variables and change as required.

You will need you own instance of Service Now and and HPE IMC server.

imc_user = "admin"
imc_passwd = "admin"
imc_host = "10.132.0.15"
snow_user = "admin"
snow_passwd = "xxxxxxxxxxxx"
instance = "xxxxxxxxxxxx"

Initial Release - Bi-Directional alarm management
