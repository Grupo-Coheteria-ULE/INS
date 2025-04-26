import cond_iniciales as cd
import math_aux as mat
import gyro_inercial as gy

def calc_f_b_real(f_b,w_b):
    m_Omega = gy.calc_Omega(w_b)
    f_b_real = f_b - mat.cross_product(m_Omega,mat.cross_product(m_Omega,cd.R_CM))
    return f_b_real 

def calc_fe(f_b,w_b,q_prev):
    DMC_be = gy.calc_DMC_be(w_b,q_prev)
    f_b_real = calc_f_b_real(f_b,w_b)
    f_e = mat.matrix_prod(f_b_real,DMC_be)
    return f_e

def calc_a_e(f_b,w_b,q_prev):
    f_e = calc_fe(f_b,w_b,q_prev)
    a_e = f_e + [0,0,cd.G]
    return a_e

def calc_a_e_real(f_b,w_b,q_prev,r_prev, v_prev):
    a_e = calc_a_e(f_b,w_b,q_prev)
    m_Edef_to_NED = mat.edef_to_ned(lat0,long0)
    correct_cent= (cd.RE+ r_prev[2])*(cd.OMEGA**2)*[cos(lat),0,cos(lat)**2]
    correct_coriolis = 2*mat.cross_product(mat.matrix_prod([0,0,cd.OMEGA],m_Edef_to_NED),v_prev)
    a_e_real = a_e - correct_cent - correct_coriolis
    return a_e_real

def calc_v_e(f_b,w_b,q_prev,r_prev, v_prev):
    a_e_real = calc_a_e_real(f_b,w_b,q_prev,r_prev, v_prev)
    v_delta = mat.intg(a_e_real)
    v_e = v_prev + v_delta
    return v_e

def calc_r_e(f_b=0, w_b=0, q_prev=0, r_prev=0, v_prev=0, v_i=None):
    if v_i != None:
        v_e = v_i
    else:
        v_e = calc_v_e(f_b,w_b,q_prev,r_prev, v_prev)

    r_delta = mat.intg(v_e)
    r_e = r_prev + r_delta
    return r_e 

