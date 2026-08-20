# import numpy as np
import pandas as pd
from .merger_tree_as_dataframe import data as merger_tree_data
from .exsitu_particles_by_peak_mass_index import data as exsitu_particles_data

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
        
        print('Access particle_history data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index
        
            

    def access(self) -> None:
        exsitu_by_peak_mass_index = exsitu_particles_data(self.__output_file_path,
                                                          self.__list_directory,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__halo,
                                                          self.__radius,
                                                          self.__peak_mass_index).access()

        tree, _ = merger_tree_data(self.__tree_directory, self.__snap_num).access()

        exsitu_merged_with_tree = pd.merge(exsitu_by_peak_mass_index[exsitu_by_peak_mass_index['PeakMassIndex'] == self.__peak_mass_index], tree, left_on='RootIndex', right_on='FirstProgenitor', how='inner')

        print(f'exsitu_merged_with_tree has {len(exsitu_merged_with_tree)} records')

        particles_grouped = exsitu_merged_with_tree[['BirthSnapshot', 'ParticleID']]
        particles_grouped = particles_grouped.groupby(['BirthSnapshot'])

        snapshots_grouped = {}

        for _, grouped in particles_grouped:
            
            particles = grouped['ParticleID']

            for particle in particles:
                
                particle_data = exsitu_merged_with_tree[exsitu_merged_with_tree['ParticleID'] == particle]

                descendant = particle_data['Descendant'].iloc[0]

                snapshots_grouped = self.navigate_tree(tree, particle, descendant, snapshots_grouped)

        return snapshots_grouped, exsitu_by_peak_mass_index

    def navigate_tree(self, tree, particle, descendant, snapshots_grouped):
        
        particle_tree_record = tree[tree['FirstProgenitor'] == descendant]

        descendants = particle_tree_record['Descendant']
        
        if len(descendants) > 0:
            descendant = particle_tree_record['Descendant'].iloc[0]
            tree_snapshot_number = particle_tree_record['SnapshotNumber'].iloc[0]
            subhalo_index = particle_tree_record['SubhaloNumber'].iloc[0]

            if particle == 8796128062993:
                print(f'particle = {particle}; snapshot = {tree_snapshot_number}; subhalo = {subhalo_index}')
                print(particle_tree_record)

            if tree_snapshot_number in snapshots_grouped.keys():
                snapshots_grouped[tree_snapshot_number].append((subhalo_index, particle))
            else:
                snapshots_grouped[tree_snapshot_number] = [(subhalo_index, particle)]

            if descendant > -1:
                snapshots_grouped = self.navigate_tree(tree, particle, descendant, snapshots_grouped)

        return snapshots_grouped