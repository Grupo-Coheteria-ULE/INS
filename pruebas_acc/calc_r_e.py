from libs import lineal_inercial as li
from libs import cond_iniciales as cd
import pandas as pd

use_data = False
i=1

#INPUTS
w_bx =[]; w_by = []; w_bz = []
df_w_b = [w_bx, w_by, w_bz]

f_bx =[]; f_by = []; f_bz = []
df_f_b = [f_bx, f_by, f_bz]

#VECTORES DE ESTADO
#Quaternion
q0 = []; q1 = []; q2 = []; q3 = []
q=[q0, q1, q2, q3]
q[0] = cd.Q0

#Velocity
v0 = []; v1 = []; v2 = []
v = [v0, v1, v2]
v[0] = cd.V0

#Position
r0 = []; r1 = []; r2 = []
r = [r0, r1, r2]
r[0] = cd.R0


if use_data == True:
    #READ DATA
    data_w = pd.read_csv(r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_gyro.csv')
    data_f = pd.read_csv(r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_accel_gon.csv')

    t_w = data_w['t'].tolist()
    df_w_b[0] = data_w['wx'].tolist()
    df_w_b[1] = data_w['wy'].tolist()    
    df_w_b[2] = data_w['wz'].tolist()

    t_f = data_f['t'].tolist()
    df_f_b[0] = data_f['ax'].tolist()
    df_f_b[1] = data_f['ay'].tolist()
    df_f_b[2] = data_f['az'].tolist()

else:

    df_w_b = [
        [0.1,0.2],
        [0.4,0.5],
        [0.7,0.8]]
    
    df_f_b = [
        [0.1,0.2],  
        [0.4,0.5],
        [0.7,0.8]]


w_b = [df_w_b[0][i],df_w_b[1][i],df_w_b[2][i]]
f_b = [df_f_b[0][i],df_f_b[1][i],df_f_b[2][i]]


r[i+1] = li.calc_r_e(f_b,w_b,q[i],r[i],v[i])
print(r[i+1])