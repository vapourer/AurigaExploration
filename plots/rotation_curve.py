import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self, file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('New rotation_curve plot')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def create(self) -> None:
        vbinstars, edges, _, _, _ = data_access.rotation_curve.data(self.__file_path, self.__snap_num,
                                                                 self.__part_type).access()

        _, ax1 = plt.subplots(1, 1, figsize=(6, 4.5), tight_layout=True)
        ax1.plot(0.5*(edges[:-1]+edges[1:])*1e3, vbinstars)
        ax1.set_xlabel('$\\rm R[kpc] $')
        ax1.set_ylabel('$\\rm{V_{circ}[km/s]}$')
        plt.savefig(f'./output/{self.__halo}/original_plots/RotationCurve_{self.__snap_num}.png')