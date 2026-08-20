import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self, file_path: str, snap_num: int, halo: str) -> None:
        print('New satellites_within_r200_stars_and_gases plot')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__halo = halo

    def create(self) -> None:
        distance, distance_star, distance_gas, _, mass, smass, gmass \
            = data_access.satellites_within_r200_stars_and_gases.data(self.__file_path, self.__snap_num).access()

        _, ax1 = plt.subplots(1, 1, figsize=(6, 4.5), tight_layout=True)

        all = ax1.scatter( distance, np.log10(mass*1e10), color='b')       
        stars = ax1.scatter( distance_star, np.log10(smass*1e10), color='g')      
        gases = ax1.scatter( distance_gas, np.log10(gmass*1e10), color='orange' )

        plt.xlabel('Distance')
        plt.ylabel('Mass')
        plt.legend([all, stars, gases], ['All', 'Stars', 'Gases'])
        plt.savefig(f'./output/{self.__halo}/original_plots/SatellitesWithinR200StarsAndGases_{self.__snap_num}.png')