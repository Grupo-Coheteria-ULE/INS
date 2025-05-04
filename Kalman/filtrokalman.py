import numpy as np

class KalmanFilterCombined:
    def __init__(self):
        
        # Matrices de transición
        self.F = np.eye(6)
        
        # Matrices de control (nula en este caso)
        self.B = np.zeros((6, 3))
        
        # Matrices de observación
        self.H = np.eye(6)
        
        # Covarianza del ruido del proceso
        self.Q = np.zeros((6, 6))
        self.Q[:3, :3] = np.eye(3) * 0.1  # Acelerómetro
        self.Q[3:, 3:] = np.eye(3) * 0.2  # Giroscopio
        
        # Covarianza del ruido de la observación
        self.R = np.zeros((6, 6))
        self.R[:3, :3] = np.eye(3) * 0.1  # Acelerómetro
        self.R[3:, 3:] = np.eye(3) * 0.2  # Giroscopio
        
        # Estado inicial
        self.x = np.zeros(6)
        
        # Covarianza inicial
        self.P = np.eye(6)

    def predict(self, u):
        # Predicción del estado
        self.x = self.F @ self.x + self.B @ u
        
        # Predicción de la covarianza
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z):
        # Ganancia de Kalman
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Actualización del estado
        self.x = self.x + K @ (z - self.H @ self.x)
        
        # Actualización de la covarianza
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P @ (I - K @ self.H).T + K @ self.R @ K.T


    def filter(self, accelerations, angular_velocities):
        filtered_accelerations = []
        filtered_angular_velocities = []

        for acc, ang_vel in zip(accelerations, angular_velocities):
            # Convertir listas a np.array si no lo son
            if not isinstance(acc, np.ndarray):
                acc = np.array(acc)
            if not isinstance(ang_vel, np.ndarray):
                ang_vel = np.array(ang_vel)
            
            u = np.zeros(3)  # Entrada de control nula
            z = np.concatenate((acc, ang_vel))  # Observación combinada

            self.predict(u)
            self.update(z)

            filtered_accelerations.append(self.x[:3])
            filtered_angular_velocities.append(self.x[3:])

        return np.array(filtered_accelerations), np.array(filtered_angular_velocities)

# Ejemplo de uso
if __name__ == "__main__":

    kf_combined = KalmanFilterCombined()

    # Simulación de datos
    accelerations = [np.array([0.1, 0.2, 0.3]), np.array([0.2, 0.3, 0.4]), np.array([0.3, 0.4, 0.5])]
    angular_velocities = [np.array([0.01, 0.02, 0.03]), np.array([0.02, 0.03, 0.04]), np.array([0.03, 0.04, 0.05])]

    filtered_accelerations, filtered_angular_velocities = kf_combined.filter(accelerations, angular_velocities)

    print("Aceleraciones filtradas:", filtered_accelerations)
    print("Velocidades angulares filtradas:", filtered_angular_velocities)
