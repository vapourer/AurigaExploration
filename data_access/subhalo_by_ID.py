from .subhalo_as_dataframe import data as subhalo_data
import pandas as pd

class data:
    def __init__(self, file_path: str, snap_num: int, subhalo_index: int) -> None:
        print('Access subhalo_by_ID data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__subhalo_index = subhalo_index

    def access(self):

        subhalo = subhalo_data(self.__file_path, self.__snap_num).access()
        return subhalo.iloc[self.__subhalo_index]
