import numpy as np
import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, tree_file_path: str, snap_num: int,
                 part_type: int, halo: str, subhalo_id: int, radius: float) -> None:
        print('Generate gas_history_specify_radius output')
        self.__file_path = file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__subhalo_id = subhalo_id
        self.__group_id = 0
        self.__fields = ['SnapNum', 'SubhaloNumber', 'SubhaloMassType', 'SubhaloPos', 'SubhaloHalfmassRadType', 'Redshift']
        self.__radius = radius

    def output(self) -> None:

        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()

        tree, original_tree = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()

        subhalo_history = original_tree.GetObjectHistoryFromSubhaloID(self.__subhalo_id,
                                                                      self.__snap_num,
                                                                      self.__group_id,
                                                                      self.__fields,
                                                                      mainprogonly=True)

        print()
        print('subhalo_history')
        print(subhalo_history)
        print()

