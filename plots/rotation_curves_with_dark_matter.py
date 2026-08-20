import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self, file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('New rotation_curves_with_dark_matter plot')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def create(self) -> None:
        Rbin, vbinstars, vbindm, Vcirc = data_access.rotation_curves_with_dark_matter.data(self.__file_path,
                                                                                           self.__snap_num,
                                                                                           self.__part_type).access()

        _, ax1 = plt.subplots(1, 1, figsize=(6, 4.5), tight_layout=True)
        ax1.plot(Rbin*1e3, vbinstars)
        ax1.plot(Rbin*1e3, vbindm)
        ax1.plot(Rbin*1e3, Vcirc)
        plt.savefig(f'./output/{self.__halo}/original_plots/RotationCurvesDarkMatterAdded_{self.__snap_num}.png')