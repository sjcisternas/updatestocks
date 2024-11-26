# Update stock values automatically

This script was created with the purpose of automatically updating the stock values you hold. The script is designed to be used with Google Sheets, so I recommend the following:

1. Have a Google account.
2. Keep your own record of the stocks you hold (including quantity, type, unit value, total value per type, and total value).

The values that are updated here are:

1. The value of the US dollar vs. the Argentine peso (MEP Dollar).
2. Values of requested CEDEARs (in Argentine pesos and in US dollars).
3. Values of requested stocks (in US dollars, according to NASDAQ).

## User guide
### 1. Google credentials
In order to access your Google account and use the script to update your Google Sheet, you must obtain a .json file with the access credentials. This file must be saved in the same folder where you will store this Python file. The credentials you need to obtain should be for a service account.

Once the service account is created and the credentials are obtained, you need to go to the desired Google Sheet and grant edit permissions to the created service account (you can find this account under the "client_email" property of the downloaded .json file).

Guide to obtain Google credentials and enable Google Drive API and Google Sheets API: [Google Developers Guide](https://developers.google.com/workspace/guides/create-credentials?hl=es-419)

### 2. REPLACE
Each line with the comment "# REPLACE" indicates where you need to enter the corresponding information. For example, in the block below, it specifies that on line 77, you need to provide a list of the stocks or securities you wish to track.
```
76. # Stock and values lists
77. stocks = 'Provide here a list with the stocks' # REPLACE
78. values = []
79. cedearValuesUSD = []
80. cedearValues = []
81. usd = USDvalue()
```
#### Full list of lines to complete:
- **Line 73 and 74:** The Google Sheet ID can be found in the URL of your Google Sheet file. The ID should be entered as a string. On line 74, enter the name of the sheet you wish to work with, in **string** format. For example:
    - URL: https://docs.google.com/spreadsheets/d/1rNDPKNAwbRF6tAzbjxiKZ4GSQ60evi4HKg/edit?gid=199041647#gid=1990741647
    - ID: 1rNDPKNAwbRF6tAzbjxiKZ4GSQ60evi4HKg
 ```
73. spreadsheet = gc.open_by_key('1rNDPKNAwbRF6tAzbjxiKZ4GSQ60evi4HKg') 
74. worksheet = spreadsheet.worksheet('Sheet1') 
```
- **Line 77:** Explained above. For example:
 ```
77. stocks = ['TSLA', 'AAPL', 'NVDA']
```
- **Line 97 y 98:** These lines define the actions to take in case the stock value is not found. You can assign a default value in case it is not found, or recalculate it as you wish.
```
96. if value == 'Value not found':
97.     calcValue = 'Here you should calculate the stock value as you wish' # REPLACE
98.     worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the left you move', calcValue) # REPLACE
99. else:
100.     worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the left you move', value) # REPLACE
```
- **Line 100, 108 y 116:** In these lines, you need to specify where you want to store the stock value. In this loop, it looks for the cell where the stock code is stored (e.g., TSLA). From that location, it will move to the right by the number of cells you indicate in line 100, and then store the corresponding stock value. For example:
```
93. for stock, value in values.items():
94.     cell = worksheet.find(stock)
95.     if cell:
96.         if value == 'Value not found':
97.             calcValue = 'Here you should calculate the stock value as you wish' # REPLACE
98.             worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the left you move', calcValue) # REPLACE
99.         else:
100.            worksheet.update_cell(cell.row, cell.col + 1, value)
101.    else:
102.        print(f'{stock} not found in the sheet provided.')
```
- **Line 121:** Here you must provide the cell where you want to store the MEP dollar value. If you do not wish to store the value, you can delete this line of code. The cell location must be entered as a **string**. For example:
```
121. worksheet.update_acell('M1', usd)
```
### 3. Automate Script Execution
The automatic execution of the script at your desired recurrence can be set up using the Windows Task Scheduler. If you are a Linux user, you can use CRON.
- [Windows Task Scheduler User Guide](https://learn.microsoft.com/es-es/windows/win32/taskschd/about-the-task-scheduler)
- [CRON user guide](https://cronitor.io/guides/cron-jobs)