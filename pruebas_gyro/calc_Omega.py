from libs import gyro_inercial as gi 
import pandas as pd

use_data = False
i=1

if use_data == True:
    #INPUTS
    w_bx =[]; w_by = []; w_bz = []
    df_w_b = [w_bx, w_by, w_bz]

    #READ DATA
    data_w = pd.read_csv(r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_gyro.csv')

    t_w = data_w['t'].tolist()

    df_w_b[0] = data_w['wx'].tolist()
    df_w_b[1] = data_w['wy'].tolist()    
    df_w_b[2] = data_w['wz'].tolist()

else:
    df_w_b = [
        [0.1,0.2],
        [0.4,0.5],
        [0.7,0.8]]


w_b = [df_w_b[0][i],df_w_b[1][i],df_w_b[2][i]]
M_omega = gi.calc_Omega(w_b)

print(w_b[1])
print(M_omega)