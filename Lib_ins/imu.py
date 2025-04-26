import pandas as pd
import cond_iniciales as cd

########
class accelerometer():
    def __init__(self,data_path):
        self.t_f = []
        self.f_bx =[]; self.f_by = []; self.f_bz = []
        self.df_f_b = [self.f_bx, self.f_by, self.f_bz]

        self.data_f = pd.read_csv(data_path)
    pass
    def read_data(self):
        self.t_f = self.data_f['t'].tolist()
        self.df_f_b[0] = self.data_f['ax'].tolist()
        self.df_f_b[1] = self.data_f['ay'].tolist()
        self.df_f_b[2] = self.data_f['az'].tolist()
        #return self.df_f_b
    pass
    #def_kalmann_filter(self):
    #pass

class gyroscope():
    def __init__(self,data_path):
        self.t_w = []
        self.w_bx =[]; self.w_by = []; self.w_bz = []
        self.df_w_b = [self.w_bx, self.w_by, self.w_bz]
        self.data_w = pd.read_csv(data_path)
    pass
    def read_data(self):
        self.t_w = self.data_w['t'].tolist()
        self.df_w_b[0] = self.data_w['wx'].tolist()
        self.df_w_b[1] = self.data_w['wy'].tolist()    
        self.df_w_b[2] = self.data_w['wz'].tolist()
        #return self.df_w_b
    pass
    #def_kalmann_filter(self):
    #pass

class IMU:
    def __init__(self, n_acc=1, n_gyro=1, acc_paths=None, gyro_paths=None): 
               #(self, n_acc(int), n_gyro(int), acc_paths(list), gyro_paths(list))
        """Inicializa el IMU con múltiples acelerómetros y giroscopios."""
        
        # Si no se proporcionan rutas, usar listas vacías
        self.acc_paths = acc_paths if acc_paths else [None] * n_acc
        self.gyro_paths = gyro_paths if gyro_paths else [None] * n_gyro
        
        # Crear listas de acelerómetros y giróscopos
        self.accelerometer = [accelerometer(self.acc_paths[i]) for i in range(n_acc)]
        self.gyroscopes = [gyroscope(self.gyro_paths[i]) for i in range(n_gyro)]

    def read_all_data(self):
        """Lee datos de todos los acelerómetros y giroscopios."""
        #con el for seguardan en self.accelerometers[i].read_data()
        for acc in self.accelerometer:
            acc.read_data()
        for gyro in self.gyroscopes:
            gyro.read_data()

    def print_all_data(self):
        """Imprime los datos de todos los acelerómetros y giroscopios."""
        for acc in self.accelerometer:
            print(acc.t_f)
            print(acc.df_f_b)
        for gyro in self.gyroscopes:
            print(gyro.t_w)
            print(gyro.df_w_b)


