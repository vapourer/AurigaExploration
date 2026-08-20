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
        
        print('Generate masses_from_particle_history output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index            

    def output(self) -> None:        
        
        snapshots_grouped, exsitu_by_peak_mass_index = data_access.masses_from_particle_history.data(self.__output_file_path,
                                                                                                     self.__list_directory,
                                                                                                     self.__tree_directory,
                                                                                                     self.__snap_num,
                                                                                                     self.__part_type,
                                                                                                     self.__halo,
                                                                                                     self.__radius,
                                                                                                     self.__peak_mass_index).access()
        
        exsitu_particles = exsitu_by_peak_mass_index['ParticleID']

        lines = []

        print()
        
        for key in snapshots_grouped.keys():
        
            disc = data_access.snapshot_raw_as_dataframe.data(self.__output_file_path, key, self.__part_type).access()

            intersection = pd.Index(exsitu_particles).intersection(pd.Index(disc['ParticleID']))

            lines.append(f'For snapshot {key}: snapshots_grouped count = {len(snapshots_grouped[key])}; intersection count = {len(intersection)}\n')

            # print(f'For snapshot {key}: snapshots_grouped count = {len(snapshots_grouped[key])}; intersection count = {len(intersection)}')

        print()

        with open(f'./output/halo_6/merger_tree_subhalo_search/back_to_particles/SnapshotGroupsDiscIntersection_{self.__peak_mass_index}.txt', 'w') as file:
            file.writelines(lines)
