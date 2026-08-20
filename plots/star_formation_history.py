import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:

    def __init__(self, file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('Create star_formation_history plot')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def create(self) -> None:
        snapobj, ages = data_access.star_formation_history.data(self.__file_path, self.__snap_num,
                                                                self.__part_type).access()
        
        plt.hist(ages, bins=40, range=[0, 14], weights=snapobj.data['GFM_InitialMass']/(14/40)*1e10/1e9)
        plt.xlabel('$\\rm age $')
        plt.ylabel('$\\rm{sfr \, [M_{\odot}yr^{-1}]}$')
        plt.savefig(f'./output/{self.__halo}/original_plots/StarFormationHistory_{self.__snap_num}.png')

