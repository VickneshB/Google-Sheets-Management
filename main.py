# importing the required libraries
import gspread
import pandas as pd
import requests
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
from datetime import date
today = date.today()
import sys

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Details of the Google Sheet
SAMPLE_SPREADSHEET_ID_input = '16I939Q_1ZBmYigJxQnrQWQLKS40QAGmJbaNd3948n84'
SAMPLE_RANGE_NAME = 'A1:AA1000'

textColor = '\033[91m'
textEnd = '\033[0m'

# Exporting the Changes to the Sheet
def Export_Data_To_Sheets(df, lineNumber):
	newDF = df.loc[lineNumber, : ]
	response_date = service.spreadsheets().values().update(
	spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
	valueInputOption='RAW',
	range='A' + str(lineNumber+2) + ':AA' + str(lineNumber+2),
	body=dict(
	majorDimension='ROWS',
	values=[newDF.T.reset_index().T.values.tolist()[1][:]])
	).execute()

def main():
	global values_input, service
	updateCount = 0
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES) # Downloaded JSON file from our sheet
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	# Call the Sheets API
	sheet = service.spreadsheets()
	result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
								range=SAMPLE_RANGE_NAME).execute()
	values_input = result_input.get('values', [])

	if not values_input and not values_expansion:
		print('No data found.')

	df=pd.DataFrame(values_input[1:], columns=values_input[0])

	links = df['Link']

	for i in range(len(links)):
		if links[i] is not None and links[i] != 'None':
			try:
				request = requests.get(links[i])
				if request.status_code != 404:
					print("Job Number", i, ":", 'Web site exists')
				else:
					print("Job Number", i, ":", 'Web site does not exist') 
					if df['Result'][i] != "Rejected" and df['Company Name'][i] is not None:
						df['Result'][i] = 'Rejected'
						df['Interview/Coding?'][i] = 'No'
						df['Date Replied'][i] = str(today.strftime("%m/%d/%Y"))
						updateCount = updateCount + 1
						Export_Data_To_Sheets(df, i)
						print('\033[91m' + "Job role no.", i, "was Updated" + '\033[0m')
			except:
				print("Job Number", i, ":","Not a URL, No action taken")
		else:
			print("Job Number", i, ":", "Web site does not exist")	
			if df['Result'][i] != "Rejected" and df['Company Name'][i] is not None:
				df['Result'][i] = 'Rejected'
				df['Interview/Coding?'][i] = 'No'
				df['Date Replied'][i] = str(today.strftime("%m/%d/%Y"))
			if df['Company Name'][i] is not None:
				df['Link'][i] = 'N/A'
				updateCount = updateCount + 1
				Export_Data_To_Sheets(df, i)
				print('\033[91m' + "Job role no.", i, "was Updated" + '\033[0m')

	print("Total of updates made:", updateCount)


if __name__ == "__main__":
	main()
