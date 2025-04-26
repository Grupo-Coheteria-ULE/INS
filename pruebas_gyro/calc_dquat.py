from libs import gyro_inercial as gi
from libs import cond_iniciales as cd
import pandas as pd

use_data = False
i=0

#INPUTS
w_bx =[]; w_by = []; w_bz = []
df_w_b = [w_bx, w_by, w_bz]

q0 = []; q1 = []; q2 = []; q3 = []
q=[q0, q1, q2, q3]
q[0] = cd.Q0

if use_data == True:

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
print(q[i])

dq = gi.calc_dquat(w_b,q[i])

print(w_b[1])
print(dq)   