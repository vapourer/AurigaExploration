import numpy as np
from .satellites import data as satellites_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access satellites_within_r200 data')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def access(self):
        distance, r200, mass, subobj = satellites_data(self.__file_path, self.__snap_num).access()
        distance_index, = np.where( (distance <= r200) & (distance > 0) )
        return distance[distance_index], r200, mass[distance_index], subobj