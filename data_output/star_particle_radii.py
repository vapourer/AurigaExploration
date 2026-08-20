import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Generate star_particle_radii output')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def output(self) -> None:
        _, _, _, subobj, star_radius = data_access.rotation_curve.data(self.__file_path, self.__snap_num,
                                                                       self.__part_type).access()
        
        print()
        print('Star particle radii')
        print(star_radius,subobj.data['Group_R_Crit200'][0])
        print()