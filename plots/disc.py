import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:

    def __init__(self, file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('New disc plot')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def create(self) -> None:
        snapobj, _ = data_access.disc.data(self.__file_path, self.__snap_num, self.__part_type).access()

        n, xedges, yedges = np.histogram2d(snapobj.data['Coordinates'][:,2], snapobj.data['Coordinates'][:,1],
                                           bins=(500,500), range=[[-0.05, 0.05],[-0.05, 0.05]])

        xbin = 0.5 * (xedges[:-1] + xedges[1:])
        ybin = 0.5 * (yedges[:-1] + yedges[1:])
        xc, yc = np.meshgrid(xbin, ybin)

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), tight_layout=True)
        ax1.set_aspect(1)
        ax1.contourf( xc, yc, np.log10(n.T), cmap='magma')

        n, xedges, yedges = np.histogram2d(snapobj.data['Coordinates'][:,2], snapobj.data['Coordinates'][:,0],
                                           bins=(500,500), range=[[-0.05, 0.05],[-0.05, 0.05]])
        
        ax2.contourf( xc, yc, np.log10(n.T), cmap='magma')
        plt.savefig(f'./output/{self.__halo}/original_plots/DiscPlots_{self.__snap_num}.png')
        