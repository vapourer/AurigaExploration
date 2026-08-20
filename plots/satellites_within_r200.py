import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self, file_path: str, snap_num: int, halo: str) -> None:
        print('New satellites_within_r200 plot')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__halo = halo

    def create(self) -> None:
        distance, _, mass, _ = data_access.satellites_within_r200.data(self.__file_path, self.__snap_num).access()

        _, ax1 = plt.subplots(1, 1, figsize=(6, 4.5), tight_layout=True)
        plt.xlabel('Distance')
        plt.ylabel('Mass')
        ax1.scatter( distance, np.log10(mass*1e10) )
        plt.savefig(f'./output/{self.__halo}/original_plots/SatellitesWithinR200MassDistance_{self.__snap_num}.png')