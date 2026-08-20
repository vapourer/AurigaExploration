import numpy as np
import data_access
from data_access import *

class data:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 tree_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: int,
                 radius: float,                 
                 peak_mass_index: int) -> None:
        
        print('Generate merger_tree_subhalo_search_by_peak_mass_index output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index        

    def output(self) -> None:
        indexed_tree = data_access.merger_tree_subhalo_search.data(self.__output_file_path,
                                                              self.__list_directory,
                                                              self.__tree_directory,
                                                              self.__snap_num,
                                                              self.__part_type,
                                                              self.__halo,
                                                              self.__radius,                                                              
                                                              self.__peak_mass_index).access()
        
        print()
        print(f'indexed_tree ({len(indexed_tree)})')
        print(indexed_tree)
        print()

        indexed_tree.to_csv(f'./output/halo_6/merger_tree_subhalo_search/MergerTreeSubhaloSearchByPeakMassIndex_Full_{self.__snap_num}_{self.__peak_mass_index}.csv', index=False)