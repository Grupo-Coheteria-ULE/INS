#Este es el script principal en el que se incluiran todos los sensores

import pandas as pd
from libs import imu_sensor as av

# Rutas de los archivos CSV
gyro_path = r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_gyro.csv'
accel_path = r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_accel_gon.csv'

# Crear instancia de IMU con 1 acelerómetro y 1 giroscopio
imu = av.IMU(n_acc=1, n_gyro=1, acc_paths=[accel_path], gyro_paths=[gyro_path])

# Leer los datos
imu.read_all_data()

# Imprimir los datos
imu.print_all_data()  

imu.INS()