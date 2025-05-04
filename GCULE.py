#Esta será la "librería" de funciones que se utilizará para el procesamiento de datos de los sensores de la avionica del grupo de cohetería de la Universidad de León.

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
from math import pi
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.spatial.transform import Rotation as R
from pykalman import KalmanFilter
import matplotlib.pyplot as plt


#seleccionar archivo mediante una ventana de inspecconar
def seleccionar_archivo():
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    file_path = askopenfilename(title="Seleccionar archivo TXT o CSV", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    return file_path
#calcular offsets en otro archivo de datos
def calcular_offsets():
    # Seleccionar el archivo
    file_path = seleccionar_archivo()
    # Leer datos del archivo seleccionado con el separador ';'
    data = pd.read_csv(file_path, sep=';', skipinitialspace=True)
    
    # Eliminar espacios en los nombres de las columnas
    data.columns = data.columns.str.strip()
    
    # Mostrar los nombres de las columnas y las primeras filas del dataframe
    print("Columnas en el archivo:", data.columns)
    print(data.head())
    
    ax1_offset = data['ax1'].tolist() if 'ax1' in data.columns else []
    ay1_offset = data['ay1'].tolist() if 'ay1' in data.columns else []
    az1_offset = data['az1'].tolist() if 'az1' in data.columns else []
    gx1_offset = data['gx1'].tolist() if 'gx1' in data.columns else []
    gy1_offset = data['gy1'].tolist() if 'gy1' in data.columns else []
    gz1_offset = data['gz1'].tolist() if 'gz1' in data.columns else []
    temp_offset = data['temp'].tolist() if 'temp' in data.columns else []
    
    #calcular las medias de los datos
    ax1_offset = np.mean(ax1_offset)
    ay1_offset = np.mean(ay1_offset)
    az1_offset = np.mean(az1_offset)
    gx1_offset = np.mean(gx1_offset)
    gy1_offset = np.mean(gy1_offset)
    gz1_offset = np.mean(gz1_offset)
                         
    return ax1_offset , ay1_offset , az1_offset , gx1_offset , gy1_offset , gz1_offset, temp_offset 
#Integrador para las listas de datos
def integratelist(lista, Tiempos):
    # Regla de Simpson con ajuste de pesos en el nodo final
    N = len(lista)
    integral = 0
    integral_list = [0] * N
    integral_list[0] = integral
    for i in range(1, N-1, 2):
        h = (Tiempos[i+1] - Tiempos[i-1]) / 2
        integral += (h / 3) * (lista[i-1] + 4 * lista[i] + lista[i+1])
        integral_list[i] = integral
        integral_list[i+1] = integral  # Asegura que la lista tenga el mismo tamaño
    
    # Ajuste de pesos para el último intervalo
    h = (Tiempos[-1] - Tiempos[-2])
    integral += (h / 2) * (lista[-2] + lista[-1])
    integral_list[-1] = integral
    
    return integral_list

#cambiar el sistema de referencia para las aceleraciones
def integrar_cuaterniones(quat_list):
    # Inicializar el cuaternión acumulado
    acumulado = R.from_quat([0, 0, 0, 1])  # Cuaternión identidad
    acumulados = []

    for quat in quat_list:
        r = R.from_quat(quat)
        acumulado = acumulado * r
        acumulados.append(acumulado.as_quat())

    return acumulados

def transformar_aceleraciones(roll_list, pitch_list,yaw_list , acc_x, acc_y, acc_z):
    # Inicializar una lista para almacenar los cuaterniones
    quaternions = []

    # Calcular los cuaterniones para cada conjunto de ángulos de Euler
    for yaw, pitch, roll in zip(yaw_list, pitch_list, roll_list):
        # Crear un objeto de rotación a partir de los ángulos de Euler
        r = R.from_euler('zyx', [yaw, pitch, roll])
        # Convertir a cuaternión y agregar a la lista
        quaternions.append(r.as_quat())

    # Integrar los cuaterniones de forma acumulativa
    quaterniones_acumulados = integrar_cuaterniones(quaternions)
    # Inicializar listas para almacenar las aceleraciones transformadas
    transformed_acc_x = []
    transformed_acc_y = []
    transformed_acc_z = []
    
    # Aplicar cada cuaternión a las aceleraciones correspondientes
    for quat, ax, ay, az in zip(quaterniones_acumulados, acc_x, acc_y, acc_z):
        r = R.from_quat(quat)
        acc_vector = np.array([ax, ay, az])
        transformed_vector = r.apply(acc_vector)
        transformed_acc_x.append(transformed_vector[0])
        transformed_acc_y.append(transformed_vector[1])
        transformed_acc_z.append(transformed_vector[2])

    return transformed_acc_x, transformed_acc_y, transformed_acc_z

#Filtrado de datos con filtro de Kalman
def aplicar_filtro_kalman(x, y, z, T,factor_trans_covarianza,factor_obs_covarianza, plot_results=False):
    # Combinar las tres medidas en una matriz
    measurements = np.vstack((x, y, z)).T

    # Definir las matrices del filtro de Kalman
    transition_matrix = np.eye(3)
    observation_matrix = np.eye(3)
    initial_state_mean = [0, 0, 0]
    initial_state_covariance = np.eye(3)
    
    # Estimar la covarianza de transición y observación
    transition_covariance = np.eye(3) * factor_trans_covarianza
    observation_covariance = np.eye(3) * factor_obs_covarianza
    
    # Crear el filtro de Kalman
    kf = KalmanFilter(
        transition_matrices=transition_matrix,
        observation_matrices=observation_matrix,
        transition_covariance=transition_covariance,
        observation_covariance=observation_covariance,
        initial_state_mean=initial_state_mean,
        initial_state_covariance=initial_state_covariance
    )
    
    # Aplicar el filtro de Kalman
    filtered_state_means, filtered_state_covariances = kf.filter(measurements)
    
    # Aplicar el suavizado de Kalman
    smoothed_state_means, smoothed_state_covariances = kf.smooth(measurements)
    
    if plot_results:
        # Separar los datos suavizados por ejes
        xmean = smoothed_state_means[:, 0]
        ymean = smoothed_state_means[:, 1]
        zmean = smoothed_state_means[:, 2]

        # Plotear los resultados en bruto, filtrados y suavizados con respecto al tiempo T
        plt.figure(figsize=(15, 10))
        
        plt.subplot(3, 1, 1)
        plt.plot(T, x, label='Raw X')
        plt.plot(T, filtered_state_means[:, 0], label='Filtered X')
        plt.plot(T, xmean, label='Smoothed X')
        plt.xlabel('Time')
        plt.ylabel('X')
        plt.legend()
        
        plt.subplot(3, 1, 2)
        plt.plot(T, y, label='Raw Y')
        plt.plot(T, filtered_state_means[:, 1], label='Filtered Y')
        plt.plot(T, ymean, label='Smoothed Y')
        plt.xlabel('Time')
        plt.ylabel('Y')
        plt.legend()
        
        plt.subplot(3, 1, 3)
        plt.plot(T, z, label='Raw Z')
        plt.plot(T, filtered_state_means[:, 2], label='Filtered Z')
        plt.plot(T, zmean, label='Smoothed Z')
        plt.xlabel('Time')
        plt.ylabel('Z')
        plt.legend()
        
        plt.tight_layout()
        plt.show()

        # Plotear las covarianzas filtradas y suavizadas para compararlas
        filtered_variances = np.mean(filtered_state_covariances, axis=(0, 2))
        smoothed_variances = np.mean(smoothed_state_covariances, axis=(0, 2))
        
        labels = ['X', 'Y', 'Z']
        
        x = np.arange(len(labels))  # Etiquetas de los ejes
        
        width = 0.35  # Ancho de las barras
        
        fig, ax = plt.subplots()
        
        rects1 = ax.bar(x - width/2, filtered_variances, width, label='Filtered')
        rects2 = ax.bar(x + width/2, smoothed_variances, width, label='Smoothed')
        
        ax.set_xlabel('Axes')
        ax.set_ylabel('Variance')
        ax.set_title('Comparison of Filtered and Smoothed Variances')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        
        fig.tight_layout()
        
        plt.show()
    
    return filtered_state_means, smoothed_state_means