# Period-Tracker
This is a simple Period Tracker Application developed for a gym coach
This is a web-based application developed using Flask that allows users to track menstrual cycles, manage client information, and dynamically update cycle phases based on the Last Menstrual Period (LMP) and other cycle parameters.

Features
Display Database: Show the current database of clients with their cycle information.
Add New Client: Form to add a new client with details such as name, LMP, average cycle length, variability, and period duration.
Delete Client: Form to delete a client from the database using their Client ID.
Update Cycle Phases: Button to update the cycle phases for all clients based on their LMP and other parameters.
Dynamic Styling: Apply specific styles to cells in the "Current Phase" column based on the phase.

---

## Requirements:
Python 3.x
Flask
pandas

---

## Installation
If you are using the program for the first time you have to install the libraries first
```
git clone https://github.com/Youssef-216/Period-Tracker.git
cd Perdiod-Tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## Running the server
Once you have installed the dependencies you can run the app
```
cd Perdiod-Tracker
source venv/bin/activate
python3 app.py
```
