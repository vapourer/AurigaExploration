import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('New satellites_within_r200 output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> None:
        distance, r200, mass, subobj = data_access.satellites_within_r200.data(self.__file_path, self.__snap_num).access()

        print()
        print('subobj')
        print(subobj.data)
        print()

        main_pos = subobj.data['SubhaloPos'][0]
        print('main_pos=',main_pos)
        print()
        print(f'r200 = {r200}')
        print()

        print('Total number of subhalos =',len(distance))
        print()
        print('distance')
        print(distance)
        print()
        print(f'mass: {len(mass)}')
        print(mass)