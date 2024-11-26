import requests
import re
import time
from fake_useragent import UserAgent
import gspread
from bs4 import BeautifulSoup

# Function to get HTML code
def HTMLcode(url):
    ua = UserAgent()
    headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua.random,
        }
    resp = requests.get(url, headers = headers)
    time.sleep(2)
    return resp.text

# Function to get stock values
def searchStockValue(stock):
    try:
        url = f'https://www.google.com/finance/quote/{stock}:NASDAQ?hl=es'
        html = HTMLcode(url)
        regex = r'<div class="YMlKec fxKbKc">(.*?)</div>'
        stockValue = re.search(regex,html)
        if stockValue:  
            value = float(stockValue.group(1)[0:-2].replace(',','.'))
            return value  
        else:
            return 'Value not found'
    except Exception as e:
        return f'Error: {e}'

# Function to get USD MEP value
def USDvalue():
    try:
        url = 'https://dolarhoy.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        value = soup.select_one('#home_0 > div:nth-child(2) > section > div > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2)')
        if value:
            return float(value.text[1:].replace(',','.').strip())
        else:
            return 'Value not found'
    except Exception as e:
        return f'Error: {e}'
    
# Function to get CEDEAR values
def searchCedearValue(stock):
    try:
        url = f'https://www.google.com/finance/quote/{stock}:BCBA?hl=es'
        html = HTMLcode(url)
        regex = r'<div class="YMlKec fxKbKc">(.*?)</div>'
        stockValue = re.search(regex,html)
        if stockValue:  
            value = stockValue.group(1)[0:-2].replace('.','')
            value = float(value.replace(',','.'))
            return value
        else:
            return 'Value not found'
    except Exception as e:
        return f'Error: {e}'

# Access to Google service account
gc = gspread.service_account(filename='credentials.json')
spreadsheet = gc.open_by_key('your_google_sheet_id') # REPLACE
worksheet = spreadsheet.worksheet('sheet_name') # REPLACE

# Stock and values lists
stocks = 'Provide here a list with the stocks' # REPLACE
values = []
cedearValuesUSD = []
cedearValues = []
usd = USDvalue()

# Get stock values
for stock in stocks:
    values.append(searchStockValue(stock))
    cedearValues.append(searchCedearValue(stock))
    cedearValuesUSD.append(searchCedearValue(stock) / usd)
values = dict(zip(stocks, values))
cedearValues = dict(zip(stocks, cedearValues))
cedearValuesUSD = dict(zip(stocks, cedearValuesUSD))

# Update stock value
for stock, value in values.items():
    cell = worksheet.find(stock)
    if cell:
        if value == 'Value not found':
            calcValue = 'Here you should calculate the stock value as you wish' # REPLACE
            worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the right you move', calcValue) # REPLACE
        else:
            worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the right you move', value) # REPLACE
    else:
        print(f'{stock} not found in the sheet provided.')

# Update CEDEAR value in USD
for stock, value in cedearValuesUSD.items():
    cell = worksheet.find(stock)
    if cell:
        worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the right you move', value) # REPLACE
    else:
        print(f'{stock} not found in the sheet provided.')

# Update CEDEAR value in ARS
for stock, value in cedearValues.items():
    cell = worksheet.find(stock)  
    if cell:
        worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the left you move', value) # REPLACE
    else:
        print(f'{stock} not found in the sheet provided.')

# Update USD value
worksheet.update_acell('Here you must provide the cell in wich the USD value will go. e.g: "M1"', usd) # REPLACE