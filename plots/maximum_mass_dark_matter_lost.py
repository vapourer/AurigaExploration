import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self, output_file_path: str, tree_file_path: str, snap_num: int, halo: str) -> None:
        print('New maximum_mass_dark_matter_lost plot')
        self.__output_file_path = output_file_path
        self.__tree_file_path = tree_file_path
        self.__snap_num = snap_num
        self.__halo = halo

    def create(self) -> None:
        distance, fraction_lost = data_access.maximum_mass_dark_matter_lost.data(self.__output_file_path,
                                                                                 self.__tree_file_path,
                                                                                 self.__snap_num).access()

        plt.scatter(distance, fraction_lost)
        plt.savefig(f'./output/{self.__halo}/original_plots/MaximumMassDarkMatterLost_{self.__snap_num}.png')