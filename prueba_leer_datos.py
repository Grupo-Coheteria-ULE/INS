
import pandas as pd 

# INPUTS
w_b = {"x": [], "y": [], "z": []}
f_b = {"x": [], "y": [], "z": []}

# OUTPUTS
r_e = {"x": [], "y": [], "z": []}
v_e = {"x": [], "y": [], "z": []}
q = {"q0": [], "q1": [], "q2": [], "q3": []}
w_e = {"x": [], "y": [], "z": []}

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
print(f_b["x"])