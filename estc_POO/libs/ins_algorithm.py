import pandas as pd
from libs import cond_iniciales as cd
from libs import math_aux as mat

class INS:
    def __init__(self):
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
        pass
    
    ### FUNCS  GYRO ###
    def calc_Omega(self, w_b):
        M_Omega = [[0, -w_b[0], -w_b[1], -w_b[2]],
                   [w_b[0], 0, w_b[2], -w_b[1]],
                   [w_b[1], -w_b[2], 0, w_b[0]],
                   [w_b[2], w_b[1], -w_b[0], 0]]
        return M_Omega
    def calc_dquat(self, w_b, q_prev):
        M_omega = self.calc_Omega(w_b)
        dquat_i = 0.5 * mat.quat_mult([q_prev, M_omega])
        return dquat_i
    def calc_quat(self, w_b, q_prev):
        dquat = self.calc_dquat(w_b, q_prev)
        q_delta= mat.intg(dquat)
        q_i = q_prev + q_delta
        return q_i
    def calc_DMC_be(self, w_b, q_prev):
        q_i = self.calc_quat(w_b, q_prev)
        DCM_be = mat.make_DCM(q_i)
        return DCM_be
    
    ### FUNCS  ACCEL ###
    def calc_f_b_real(self, f_b, w_b):
        m_Omega = self.calc_Omega(w_b)
        f_b_real = f_b - mat.cross_product(m_Omega,mat.cross_product(m_Omega,cd.R_CM))
        return f_b_real 

    def calc_fe(self, f_b, w_b, q_prev):
        DMC_be = self.calc_DMC_be(w_b,q_prev)
        f_b_real = self.calc_f_b_real(f_b,w_b)
        f_e = mat.matrix_prod(f_b_real,DMC_be)
        return f_e

    def calc_a_e(self, f_b, w_b, q_prev):
        f_e = self.calc_fe(f_b,w_b,q_prev)
        a_e = f_e + [0,0,cd.G]
        return a_e

    def calc_a_e_real(self, f_b,w_b,q_prev,r_prev, v_prev):
        a_e = self.calc_a_e(f_b,w_b,q_prev)
        m_Edef_to_NED = mat.edef_to_ned(lat0,long0)
        correct_cent= (cd.RE+ r_prev[2])*(cd.OMEGA**2)*[cos(lat),0,cos(lat)**2]
        correct_coriolis = 2*mat.cross_product(mat.matrix_prod([0,0,cd.OMEGA],m_Edef_to_NED),v_prev)
        a_e_real = a_e - correct_cent - correct_coriolis
        return a_e_real

    def calc_v_e(self, f_b,w_b,q_prev,r_prev, v_prev):
        a_e_real = self.calc_a_e_real(f_b,w_b,q_prev,r_prev, v_prev)
        v_delta = mat.intg(a_e_real)
        v_e = v_prev + v_delta
        return v_e

    def calc_r_e(self, f_b=0, w_b=0, q_prev=0, r_prev=0, v_prev=0, v_i=None):
        if v_i != None:
                v_e = v_i
        else:
                v_e = self.calc_v_e(f_b,w_b,q_prev,r_prev, v_prev)

        r_delta = mat.intg(v_e)
        r_e = r_prev + r_delta
        return r_e 

        S