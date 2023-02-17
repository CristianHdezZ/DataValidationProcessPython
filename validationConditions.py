from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import date, timedelta, datetime


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
# Escribe aquí el ID de tu documento:
SPREADSHEET_ID = '1VLRN4f6BgjFf6aAVgI0JfEXCUMJwIzwgmRJMU_ZZYZA'

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


# Llamada a la api
result_date_inicial = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!H2:H300').execute()
result_date_final = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range='Hoja 1!I2:I300').execute()
result_price = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range='Hoja 1!J2:J300').execute()
# Extraemos values del resultado
values_date_inicial = result_date_inicial.get('values',[])
values_date_final = result_date_final.get('values',[])
values_price = result_price.get('values',[])

valueslist_date_inicial = list()
valueslist_date_inicial = values_date_inicial

valueslist_date_final = list()
valueslist_date_final = values_date_final

valueslist_price = list()
valueslist_price = values_price

total_sum_prices = int(0)
cantidad_prices = int(0)


revision_regla = [['ok']]

for i in range(len(valueslist_date_inicial)):
    for j in range(len(valueslist_date_inicial[i])):
    	fecha_inicial_str = valueslist_date_inicial[i][j]
    	fecha_inicial_split = fecha_inicial_str.split('/')
    	fecha_final_str = valueslist_date_final[i][j]
    	values_price_str = valueslist_price[i][j]
    	values_price_split = values_price_str.split(' ')
    	values_price_replace = str(values_price_split[1]).replace('.','')
    	date_inicial_object = datetime.strptime(fecha_inicial_str,'%d/%m/%Y').date()
    	date_final_object = datetime.strptime(fecha_final_str,'%d/%m/%Y').date()
    	date_final_cal = date_inicial_object + timedelta(60)
    	#print('fecha split: ',fecha_inicial_split[2])    	


    	if date_final_object==date_final_cal:
    		print("ok: ",date_final_object)
    		RANGE_DATE = 'Hoja 1!K'+str(i+2)
    		request_date = sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_DATE,valueInputOption='USER_ENTERED',body={'values':revision_regla}).execute()

    	if (int(values_price_replace)<200000) and (int(values_price_replace)>2500):
    		print('OK price: ',values_price_replace)
    		RANGE_PRICE = 'Hoja 1!L'+str(i+2)
    		RANGE_PRICES_AVERAGE = 'Hoja 1!O'+str(i+2)
    		request_price = sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_PRICE,valueInputOption='USER_ENTERED',body={'values':revision_regla}).execute()
    		request_prices_average = sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_PRICES_AVERAGE,valueInputOption='USER_ENTERED',body={'values':[[int(values_price_replace)]]}).execute()
    		total_sum_prices +=int(values_price_replace)
    		cantidad_prices +=1

    	if int(fecha_inicial_split[2])==2020:
    		print('OK fecha 2020: ',fecha_inicial_str)
    		RANGE_DATE_SPECIFIC = 'Hoja 1!M'+str(i+2)
    		request_date_specific = sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_DATE_SPECIFIC,valueInputOption='USER_ENTERED',body={'values':revision_regla}).execute()

    	if (int(fecha_inicial_split[2])==2019) and (int(fecha_inicial_split[1])==4):
    		print('OK fecha 2019 and 04: ',fecha_inicial_str,int(fecha_inicial_split[1]))
    		RANGE_BETWEEN_DATE_MONTH = 'Hoja 1!N'+str(i+2)
    		request_between_date_month = sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_BETWEEN_DATE_MONTH,valueInputOption='USER_ENTERED',body={'values':revision_regla}).execute()

    	if date_inicial_object > date_final_object:
    		print('Fecha incial es mayor que fecha final: ',date_inicial_object,' - ',date_final_object)
    		RANGE_ERROR = 'Hoja 1!P'+str(i+2)
    		request_error = sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_ERROR,valueInputOption='USER_ENTERED',body={'values':[['Fecha incial es mayor que fecha final']]}).execute()

request_prices_average_total = sheet.values().append(spreadsheetId=SPREADSHEET_ID,range='Hoja 1!O12',valueInputOption='USER_ENTERED',insertDataOption="INSERT_ROWS",body={'values':[[total_sum_prices/cantidad_prices]]}).execute()
print('cantidad: ',cantidad_prices)
