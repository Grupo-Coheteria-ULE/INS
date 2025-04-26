import lineal_inercial as li
import cond_iniciales as ci
import gyro_inercial as gi
import pandas as pd 

# INPUTS
w_b = {"x": [], "y": [], "z": []}
f_b = {"x": [], "y": [], "z": []}

# OUTPUTS
r_e = {"x": [ci.R0[0]], "y": [ci.R0[1]], "z": [ci.R0[2]]}
v_e = {"x": [ci.V0[0]], "y": [ci.V0[1]], "z": [ci.V0[2]]}
q = {"q0": [ci.Q0[0]], "q1": [ci.Q0[1]], "q2": [ci.Q0[2]], "q3": [ci.Q0[3]]}

##w_e = {"x": [], "y": [], "z": []}

#READ INPUTS
data_f = pd.read_csv(r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_accel_gon.csv')
data_w = pd.read_csv(r'C:\Users\manue\Desktop\Acctitude Flight System\Monitor Telemetría Tierra\Algoritmo_ins\Datos\dato_gyro.csv')

t_w = data_w['t'].tolist()
w_b["x"] = data_w['wx'].tolist()
w_b["y"] = data_w['wy'].tolist()    
w_b["z"] = data_w['wz'].tolist()

t_f = data_f['t'].tolist()
f_b["x"] = data_f['ax'].tolist()
f_b["y"] = data_f['ay'].tolist()
f_b["z"] = data_f['az'].tolist()


#CALCULATIONS
for i in range(1,len(w_b)):
    q[i]=li.gy.calc_quat(w_b[i],q[i-1])
    v_e[i]=li.calc_v_e(f_b[i])
    r_e[i]=li.calc_r_e(v_i = v_e[i])
    r_e[i]=li.calc_r_e(v_e[i])




