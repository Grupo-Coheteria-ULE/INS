from . import math_aux as mat
import cond_iniciales as cd

def calc_Omega(w_b):
    M_Omega = [[0, -w_b[0], -w_b[1], -w_b[2]],
               [w_b[0], 0, w_b[2], -w_b[1]],
               [w_b[1], -w_b[2], 0, w_b[0]],
               [w_b[2], w_b[1], -w_b[0], 0]]
    return M_Omega

def calc_dquat(w_b, q_prev):
    M_omega = calc_Omega(w_b)
    dquat_i = 0.5 * mat.quat_mult([q_prev, M_omega])
    return dquat_i

def calc_quat(w_b, q_prev):
    dquat = calc_dquat(w_b, q_prev)
    q_delta= mat.intg(dquat)
    q_i = q_prev + q_delta
    return q_i

def calc_DMC_be(w_b, q_prev):
    q_i = calc_quat(w_b, q_prev)
    DCM_be = mat.make_DCM(q_i)
    return DCM_be
