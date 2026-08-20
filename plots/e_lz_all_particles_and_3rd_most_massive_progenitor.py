import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import data_access
from data_access import *

class plot:
    def __init__(self, output_file_path: str, list_file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('New e_lz_all_particles_and_3rd_most_massive_progenitor plot')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def create(self) -> None:
        Lz, index, orbital_energy, id_index_prog \
            = data_access.e_lz_all_particles_and_3rd_most_massive_progenitor.data(self.__output_file_path,
                                                                                  self.__list_directory,
                                                                                  self.__snap_num,
                                                                                  self.__part_type,
                                                                                  self.__halo).access()

        _, ax = plt.subplots(1, 1, figsize=(6, 4.5), tight_layout=True)
        ax.hist2d( Lz[index], orbital_energy[index], bins=(100, 100), range=([-5, 5], [-2.2, 0.]),
                  rasterized=True, cmap='Greys', norm=LogNorm() )
        
        ax.scatter( Lz[id_index_prog], orbital_energy[id_index_prog], c='b', s=5, marker='.', linewidth=0, alpha=0.2 )

        plt.savefig(f'./output/{self.__halo}/original_plots/E_LzAllParticlesAnd3rdMostMassiveProgenitor_{self.__snap_num}.png')