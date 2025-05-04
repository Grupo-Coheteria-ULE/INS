import numpy as np

def estimate_covariance(simulated_data, real_data):
    # Transformar las listas en arrays de numpy
    simulated_data = np.array(simulated_data)
    real_data = np.array(real_data)

    # Calcular las diferencias entre los datos simulados y reales
    differences = simulated_data - real_data
    
    # Estimar la covarianza del ruido del proceso (Q)
    Q = np.cov(differences, rowvar=False)
    
    # Estimar la covarianza del ruido de la observación (R)
    R = np.cov(real_data, rowvar=False)
    
    return Q, R

# Ejemplo de uso con listas de nx6 elementos
simulated_data = np.array([
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
    [0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
    [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
])

real_data = np.array([
    [0.12, 0.22, 0.32, 0.42, 0.52, 0.62],
    [0.18, 0.28, 0.38, 0.48, 0.58, 0.68],
    [0.31, 0.41, 0.51, 0.61, 0.71, 0.81]
])

Q, R = estimate_covariance(simulated_data, real_data)

print("Covarianza del ruido del proceso (Q):", Q)
print("Covarianza del ruido de la observación (R):", R)
