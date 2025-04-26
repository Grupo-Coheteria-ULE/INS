import pandas as pd

# Ruta del archivo CSV dentro de la carpeta "Datos"
filename = r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_accel_gon.csv'

# Leer el archivo CSV con pandas
df = pd.read_csv(filename)

# Convertir las columnas a tipo float
df = df.astype(float)

# Mostrar los datos leídos
print(df)
