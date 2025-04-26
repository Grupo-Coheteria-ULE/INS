import math

def make_DCM(q):
    """Create the direction cosine matrix from the quaternion."""
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]
    DCM = [[q0**2 + q1**2 - q2**2 - q3**2, 2*(q1*q2 - q0*q3), 2*(q1*q3 + q0*q2)],
           [2*(q1*q2 + q0*q3), q0**2 - q1**2 + q2**2 - q3**2, 2*(q2*q3 - q0*q1)],
           [2*(q1*q3 - q0*q2), 2*(q2*q3 + q0*q1), q0**2 - q1**2 - q2**2 + q3**2]]
    return DCM

def quat_to_ang_TaitBryan(q): #revisar que estan bien el orden de los angulos
    """Convert a quaternion to Tait-Bryan angles."""
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]
    phi = math.atan2(2*(q0*q1 + q2*q3), 1 - 2*(q1**2 + q2**2)) 
    theta = math.asin(2*(q0*q2 - q3*q1))
    psi = math.atan2(2*(q0*q3 + q1*q2), 1 - 2*(q2**2 + q3**2))
    return phi, theta, psi

def ang_to_quat_TaitBryan(phi, theta, psi): #revisar que estan bien el orden de los angulos
    """Convert Tait-Bryan angles to a quaternion."""
    phi2 = phi/2
    theta2 = theta/2
    psi2 = psi/2
    q0 = math.cos(phi2)*math.cos(theta2)*math.cos(psi2) + math.sin(phi2)*math.sin(theta2)*math.sin(psi2)
    q1 = math.sin(phi2)*math.cos(theta2)*math.cos(psi2) - math.cos(phi2)*math.sin(theta2)*math.sin(psi2)
    q2 = math.cos(phi2)*math.sin(theta2)*math.cos(psi2) + math.sin(phi2)*math.cos(theta2)*math.sin(psi2)
    q3 = math.cos(phi2)*math.cos(theta2)*math.sin(psi2) - math.sin(phi2)*math.sin(theta2)*math.cos(psi2)
    return q0, q1, q2, q3

def edef_to_ned(lat0, long0):
    """Create the transformation matrix from ECEF to NED."""
    DCM_edef_to_ned = [[-math.sin(lat0)*math.cos(long0), -math.sin(long0), -math.cos(lat0)*math.cos(long0)],
           [-math.sin(lat0)*math.sin(long0), math.cos(long0), -math.cos(lat0)*math.sin(long0)],
           [math.cos(lat0), 0, -math.sin(lat0)]]
    return DCM_edef_to_ned

def esf_to_cart(phi, lam):
    """Create the transformation matrix from spherical to Cartesian coordinates."""
    DCM_esf_to_cart = [[math.cos(lam)*math.cos(phi), -math.cos(lam)*math.sin(phi), -math.sin(lam)],
                       [math.sin(lam)*math.cos(phi), -math.sin(lam)*math.sin(phi), math.cos(lam)],
                       [math.sin(phi), math.cos(phi), 0]]
    return DCM_esf_to_cart
