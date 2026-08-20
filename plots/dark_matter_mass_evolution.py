import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self, tree_file_path: str, snap_num: int, halo: str) -> None:
        print('New dark_matter_mass_evolution plot')
        self.__tree_file_path = tree_file_path
        self.__snap_num = snap_num
        self.__halo = halo

    def create(self) -> None:
        result_main = data_access.dark_matter_mass_evolution.data(self.__tree_file_path, self.__snap_num).access()

        _, ax1 = plt.subplots(1, 1, figsize=(6, 4.5), tight_layout=True)
        ax1.plot(result_main['Redshift'], result_main['SubhaloMassType'][:,:,1]*1e10)
        ax1.set_yscale('log')
        ax1.set_xscale('log')
        ax1.set_xlim(0.01,10.)
        ax1.set_ylim(1e8, 1e11)
        plt.savefig(f'./output/{self.__halo}/original_plots/DarkMatterMassEvolution_{self.__snap_num}.png')