# Google-Sheets-Management

This project was created to manage the data in a google sheet. The program will be able to read the data, modify it accordingly and then update it. I also used a URL request in this project to check whether a URL still exists. I used my google sheet in which I maintained the documentaion of the job roles I applied for. I used columns, "No., Company Name	Location, Position, Date Applied, Date Replied, Interview/Coding?, Result, Link". In this data I take the column Links and check whether each link exists. If they don't I Update the corresponding value for Date Replied to be "Today's date", Intervie/Coding? to be "No" and Result to be "Rejected". With the help of this program I will be able to check whether a job role is still on and then update my status of my application.


1.  Clone the repository
	```
	$ git clone https://github.com/VickneshB/Google-Sheets-Management.git
	```

2.  Create an virtual environment using
	```
	$ python3 -m venv  virtual environment name.
	```
3.  Run 
	```
	$ pip3 install -r requirements.txt
	```
4.  Run either of the below of your choice.
	```
	$ python3 main.py
	```
