import numpy as np
import pandas as pd
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
        
        print('Generate snapshot_subhalo_from_merger_tree output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index            

    def output(self) -> None:
        snapshots_grouped, _ = data_access.snapshots_subhalos_by_particle.data(self.__output_file_path, self.__list_directory, self.__tree_directory, self.__snap_num, self.__part_type, self.__halo, self.__radius, self.__peak_mass_index).access()
        # print(snapshots_grouped)
        # print()
        # print('snapshots_grouped: 50')
        # print(snapshots_grouped[50])
        # print()
        # print('snapshots_grouped: 52')
        # print(snapshots_grouped[52])
        # # print()
        # # print('Keys')
        # # print(snapshots_grouped.keys())
        # print()
        # print('snapshots_grouped: 247')
        # print(snapshots_grouped[247])
        print()
        print(f'snapshots_grouped: 251 ({len(snapshots_grouped[251])})')
        print(snapshots_grouped[251])
        print()

        # subhalos_per_snapshot = {}

        # for snapshot in snapshots_grouped.keys():
        #     subhalo = snapshots_grouped[snapshot][0]

        #     if snapshot in subhalos_per_snapshot.keys():
        #         subhalos_per_snapshot[snapshot].append(subhalo)
        #     else:
        #         subhalos_per_snapshot[snapshot] = [subhalo]

        # for snapshot in subhalos_per_snapshot.keys():
        #     unique_subhalos = set(subhalos_per_snapshot[snapshot])
        #     subhalo_count = len(unique_subhalos)
        #     print(f'snapshot {snapshot} has {subhalo_count} subhalos')

        # print()

