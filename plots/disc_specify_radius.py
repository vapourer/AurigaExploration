import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:

    def __init__(self, file_path: str, snap_num: int, part_type: int, radius: float, halo: str) -> None:
        print('New disc_specify_radius plot')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__radius = radius
        self.__halo = halo

    def create(self) -> None:
        bounded_disc, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__file_path, self.__snap_num,
                                                            self.__part_type, self.__radius).access()
        

        n, xedges, yedges = np.histogram2d(bounded_disc['Z'], bounded_disc['Y'],
                                           bins=(500,500), range=[[-0.05, 0.05],[-0.05, 0.05]])

        xbin = 0.5 * (xedges[:-1] + xedges[1:])
        ybin = 0.5 * (yedges[:-1] + yedges[1:])
        xc, yc = np.meshgrid(xbin, ybin)

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), tight_layout=True)
        ax1.set_aspect(1)
        ax1.contourf( xc, yc, np.log10(n.T), cmap='magma')

        n, xedges, yedges = np.histogram2d(bounded_disc['Z'], bounded_disc['X'],
                                           bins=(500,500), range=[[-0.05, 0.05],[-0.05, 0.05]])
        
        ax2.contourf( xc, yc, np.log10(n.T), cmap='magma')

        radius_kpc = int(self.__radius * 1000)
        disc_size = f'Within{radius_kpc}kpc'        

        if self.__radius < 0:
            disc_size = 'R200'

        plt.savefig(f'./output/{self.__halo}/disc/DiscPlots{disc_size}_{self.__snap_num}.png')
        