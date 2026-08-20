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
        
        print('Generate stellar_info_by_peak_mass_index output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index
        
            

    def output(self) -> None:
        exsitu_by_peak_mass_index = data_access.exsitu_particles_by_peak_mass_index.data(self.__output_file_path,
                                                              self.__list_directory,
                                                              self.__snap_num,
                                                              self.__part_type,
                                                              self.__halo,
                                                              self.__radius,                                                              
                                                              self.__peak_mass_index).access()
        
        print()
        print(f'exsitu_by_peak_mass_index ({len(exsitu_by_peak_mass_index)})')
        print(exsitu_by_peak_mass_index)
        print()

        tree, _ = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()

        print()
        print(f'tree ({len(tree)})')
        print(tree)
        print()

        exsitu_merged_with_tree = pd.merge(exsitu_by_peak_mass_index[exsitu_by_peak_mass_index['PeakMassIndex'] == self.__peak_mass_index], tree, left_on='RootIndex', right_on='FirstProgenitor', how='inner')

        print()
        print(f'exsitu_merged_with_tree ({len(exsitu_merged_with_tree)})')
        print(exsitu_merged_with_tree.columns)
        print(exsitu_merged_with_tree)
        print()

        exsitu_merged_with_tree.to_csv(f'./output/halo_6/stellar_info/StellarInfo{self.__peak_mass_index}.csv', index=False)

        particle_count = exsitu_merged_with_tree['ParticleID'].count()
        bound_first_time_min = np.min(exsitu_merged_with_tree['BoundFirstTime'])
        bound_first_time_max = np.max(exsitu_merged_with_tree['BoundFirstTime'])
        stellar_mass = np.sum(exsitu_merged_with_tree['StellarMass'])
        stellar_half_mass_radius_min = np.min(exsitu_merged_with_tree['StellarHalfMassRadius'])
        stellar_half_mass_radius_max = np.max(exsitu_merged_with_tree['StellarHalfMassRadius'])

        print(f'particle_count = {particle_count}')
        print(f'bound_first_time_min = {bound_first_time_min}')
        print(f'bound_first_time_max = {bound_first_time_max}')
        print(f'stellar_mass = {stellar_mass}')
        print(f'stellar_half_mass_radius_min = {stellar_half_mass_radius_min}')
        print(f'stellar_half_mass_radius_max = {stellar_half_mass_radius_max}')

        count = 0

        for particle in exsitu_merged_with_tree['ParticleID']:
            record = exsitu_merged_with_tree[exsitu_merged_with_tree['ParticleID'] == particle]

            if (record['BirthSnapshot'].iloc[0]) == record['SnapshotNumber'].iloc[0]:
                count += 1

        print()
        print(f'Count of exceptions = {count}')
        print()

