# Actualizá los valores de tus acciones de manera automática

Este script fue creado con el objetivo de manter actualizados, de manera automática, los valores de las acciones que posees. El script está pensado para utilizarlo con Google Sheets, por lo que recomiendo:

1. Tener una cuenta de Google.
2. Tener tu propio registro de las acciones que posees (inlcuyendo cantidad, especie, valor unitario, valor total por especie y valor total)

Los valores que se actualizan aquí son:

1. Valor del dolar estadounidense vs. el peso argentino (Dolar MEP)
2. Valores de los CEDEAR solicitados (en pesos argentinos y en dólares)
3. Valores de las acciones solicitadas (en dólares, según NASDAQ)

## Guía de uso
### 1. Google credentials
Para poder acceder a su cuenta de Google y de esta manera poder utilizar el script, y así actualizar su Google Sheet, usted debe obtener un archivo .json con las credenciales de acceso. Dicho archivo debe guardarse en la misma carpeta en donde guardará este archivo Python. Las credenciales a obtener deben ser para **cuenta de servicio**

Una vez creada la cuenta de servicio y obtenidas las credenciales, debe ir al archivo Google Sheet deseado, y otorgar permisos de editor a la cuenta de servicio creada (podrá encontrar dicha cuenta en la propiedad "client_email" del archivo .json descargado).

Guía para obtener credenciales de Google, y habilitar Google Drive API y Google Sheets API: [Google Developers Guide](https://developers.google.com/workspace/guides/create-credentials?hl=es-419)

### 2. REPLACE
Cada línea que tenga el comentario "# REPALCE" indica que usted debe ingresar la información correspondiente. Por ejemplo, en el bloque inferior se indica que en la línea 77 se debe ingresar una lista con las stocks o securities que usted desee.
```
76. # Stock and values lists
77. stocks = 'Provide here a list with the stocks' # REPLACE
78. values = []
79. cedearValuesUSD = []
80. cedearValues = []
81. usd = USDvalue()
```
#### 2.1 Lista completa de todas las líneas a completar:
- **Línea 73 y 74:** El Google Sheet ID lo encuentra en la URL de su archivo Google Sheet. El ID debe ingresarse como un **string**. En la línea 74, debe ingresar el nombre de la hoja en la que quiere trabajar, en formato **string**. Por ejemplo:
    - URL: https://docs.google.com/spreadsheets/d/1rNDPKNAwbRF6tAzbjxiKZ4GSQ60evi4HKg/edit?gid=199041647#gid=1990741647
    - ID: 1rNDPKNAwbRF6tAzbjxiKZ4GSQ60evi4HKg
 ```
73. spreadsheet = gc.open_by_key('1rNDPKNAwbRF6tAzbjxiKZ4GSQ60evi4HKg') 
74. worksheet = spreadsheet.worksheet('Sheet1') 
```
- **Línea 77:** Explicado previamente. Por ejemplo:
 ```
77. stocks = ['TSLA', 'AAPL', 'NVDA']
```
- **Línea 97 y 98:** Estas líneas son las acciones a realizar en caso de que el valor de la acción no haya sido encontrado. Usted puede asignar un valor por defecto en caso de no encontrar el valor, o calcularlo nuevamente como desee.
```
96. if value == 'Value not found':
97.     calcValue = 'Here you should calculate the stock value as you wish' # REPLACE
98.     worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the left you move', calcValue) # REPLACE
99. else:
100.     worksheet.update_cell(cell.row, cell.col + 'Here you must provide a number that represent how many cells to the left you move', value) # REPLACE
```
- **Línea 100, 108 y 116:** En estas líneas usted debe especificar en qué celda desea guardar el valor de la acción. En este loop lo que se hace es buscar en qué celda usted almacenó el código de la acción (por ejemplo: TSLA). Desde esa ubicación, se desplazará hacia la derecha la cantidad de celdas que usted indique en la línea 100, y luego se almacenará el valor de la acción correspondiente. Por ejemplo:
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
- **Línea 121:** Aquí debe proveer la celda en donde desea almacenar el valor del dolar MEP. En caso de no desear almacenar el valor del dolar, puede eliminar esta línea de código. La ubicación de la celda debe ser ingresada en formato **string**. Por ejemplo:
```
121. worksheet.update_acell('M1', usd)
```
### 3. Automatizar la ejecución del script
La ejecución automática del script según la recurrencia que usted desee, se realiza utilizando el Programador de tareas de Windows. En caso de ser usuario de Linux, puede utilzar CRON.
- [Programador de tareas de Windows user guide](https://learn.microsoft.com/es-es/windows/win32/taskschd/about-the-task-scheduler)
- [CRON user guide](https://cronitor.io/guides/cron-jobs)