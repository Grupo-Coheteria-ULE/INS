import numpy as np
import cond_iniciales as cd
import math_aux as mat


def ecef_position(rned, lat0, long0, Rearth):
    
    alt = rned[2]
    Pxecef = (cd.RE + alt) * np.cos(lat0) * np.cos(long0)
    Pyecef = (cd.RE + alt) * np.cos(lat0) * np.sin(long0)
    Pzecef = (cd.RE + alt) * np.sin(lat0)
    return np.array([Pxecef, Pyecef, Pzecef])   

def acel_centrip_coriolis(r_prev, v_prev, lat0, long0):
               
    # Obtener matriz DCM de NED a ECEF
    m_Edef_to_NED = mat.edef_to_ned(lat0, long0)
    
    # Calcular posicion en ECEF
    recef_base = ecef_position(rned, lat0, long0, cd.RE)
    recef = recef_base + mat.matrixprod(r_prev, R_ned2ecef)
    
    # Velocidad en ECEF
    vecef = mat.matrixprod(v_prev, m_Edef_to_NED)

    # Aceleracion centripeta y de Coriolis en ECEF
    a_centripeta_ecef = mat.crossproduct(np.array([0, 0, cd.OMEGA]), mat.crossproduct(np.array([0, 0, cd.OMEGA]), recef))
    a_coriolis_ecef = - 2 * mat.crossproduct(np.array([0, 0, cd.OMEGA]), vecef)

    # Convertir aceleraciones a NED
    a_centripeta_ned = mat.matrixprod(a_centripeta_ecef, m_Edef_to_NED)
    a_coriolis_ned = mat.matrixprod(a_coriolis_ecef, m_Edef_to_NED)

    return a_centripeta_ned, a_coriolis_ned