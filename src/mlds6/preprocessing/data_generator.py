import numpy as np
import keras
import h5py
import json

class DataGenerator(keras.utils.Sequence):
    '''
    Generador de datos para Keras.

    Toma un dataframe con las rutas a las imagenes procesadas (ruta_array_procesado)
    y genera batches de datos de tamaño `batch_size` con las imagenes y sus etiquetas.

    Las imagenes corresponden a los arreglos de numpy obtenidos de cada una de las
    rutas, de tamaño `dim` y número de canales `n_channels`. Cuando `mode` = "train"
    se realiza una serie de transformaciones aleatorias a las imagenes con el proposito
    de que en cada epoch el modelo vea imagenes ligeramente diferentes.

    Las etiquetas retornadas son representaciones one-hot de las etiquetas originales.

    En cada epoca se pueden pasar los datos en orden aleatorio nuevo si `shuffle=True`

    Propiedad relevante:
    - self.labels_dict: Diccionario con el mapeo entre las etiquetas originales y
        el indice de la representación one-hot. Util para determinar las etiquetas
        reales clasificadas

    '''
    def __init__(self, filepath, dataset_X="images", dataset_y="classes" ,batch_size=32, dim=(200, 200), n_channels=3, shuffle=True, mode="val/test", augmentation_params={"width_range": [-0.05, 0], "height_range": [-0.05, 0], "rotation_factor": [-0.05, 0.05], "contrast_factor": [0,0.2], "gaussian_blur_factor": [0,0.2]}, **kwargs):
        'Initialization'
        super().__init__(**kwargs)
        self.filepath = filepath
        self.hdf5_file = h5py.File(self.filepath, 'r')
        self.X_data = self.hdf5_file["images"]
        self.y_data = self.hdf5_file["classes"]
        self.dim = dim
        self.batch_size = batch_size
        self.mode = mode
        self.augmentation_params = augmentation_params

        self.index_to_class_mapping = json.loads(self.hdf5_file["classes"].attrs['index_to_class'])
        self.distinct_labels = list(self.index_to_class_mapping.values()) # Lista de etiquetas unicas ordenadas
        self.n_classes = len(self.distinct_labels) # Número de clases
        self.labels_dict = dict(zip(self.distinct_labels, range(self.n_classes))) # Mapeo de etiquetas a numero del one-hot encoding
        self.list_IDs = np.arange(self.hdf5_file["classes"].shape[0]) # Indices para identificar los datos

        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

        self.augmentation_train_fun = self.augmentation_train(**augmentation_params)
        self.augmentation_val_test_fun = self.augmentation_val_test()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        list_IDs_temp.sort() # Sort the IDs to avoid h5py error

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = self.X_data[list_IDs_temp, :, :, :]
        y = self.y_data[list_IDs_temp, :]

        if self.mode == "train":
            X = self.augmentation_train_fun(X)
        else :
            X = self.augmentation_val_test_fun(X)

        return X, y

    def augmentation_train(self, width_range, height_range, rotation_factor, contrast_factor, gaussian_blur_factor):

        augmetation_model = keras.Sequential(
            [
                keras.Input(shape=(*self.dim, self.n_channels)),
                keras.layers.Rescaling(scale=1./127.5, offset=-1),
                keras.layers.RandomContrast(contrast_factor, value_range=(-1, 1)),
                keras.layers.RandomGaussianBlur(gaussian_blur_factor, kernel_size=3,sigma=1.0,value_range=(-1,1)),
                keras.layers.RandomRotation(rotation_factor,fill_mode="constant", fill_value=-1),
                keras.layers.RandomZoom(height_factor=height_range, width_factor=width_range)
            ]
        )

        return augmetation_model

    def augmentation_val_test(self):
        augmetation_model = keras.Sequential(
            [
                keras.Input(shape=(*self.dim, self.n_channels)),
                keras.layers.Rescaling(scale=1./127.5, offset=-1),
            ]
        )

        return augmetation_model