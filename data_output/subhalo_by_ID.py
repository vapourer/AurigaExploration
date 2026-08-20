import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int, subhalo_index: int) -> None:
        print('Generate subhalo_by_ID output')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__subhalo_index = subhalo_index

    def output(self) -> None:

        subhalo = data_access.subhalo_by_ID.data(self.__file_path,
                                                 self.__snap_num,
                                                 self.__subhalo_index).access()
        
        print()
        print(f'subhalo {self.__subhalo_index}')
        print(subhalo)
        print()