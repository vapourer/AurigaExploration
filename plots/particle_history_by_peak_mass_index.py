import numpy as np
import pandas as pd
import data_access
from data_access import *

class plot:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 tree_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: int,
                 radius: float,                 
                 peak_mass_index: int) -> None:
        
        print('New particle_history_by_peak_mass_index plots')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index            

    def create(self) -> None:        
        
        snapshots_grouped = data_access.particle_history.data(self.__output_file_path,
                                                 self.__list_directory,
                                                 self.__tree_directory,
                                                 self.__snap_num,
                                                 self.__part_type,
                                                 self.__halo,
                                                 self.__radius,
                                                 self.__peak_mass_index).access()
        
        print(f'snapshots_grouped has {len(snapshots_grouped.keys())} records')
        print(f'snapshots_grouped for peak mass index 251 ({len(snapshots_grouped[251])})')
        # print(snapshots_grouped[251])
        # print(snapshots_grouped.keys())
