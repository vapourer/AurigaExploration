import numpy as np
import pandas as pd
from .merger_tree_as_dataframe import data as merger_tree_data
from .exsitu_particles_by_peak_mass_index import data as exsitu_particles_data
from .particle_history import data as particle_history_data

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
        
        print('Access masses_from_particle_history data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index
        
            

    def access(self) -> None:
        return particle_history_data(self.__output_file_path, self.__list_directory, self.__tree_directory, self.__snap_num, self.__part_type, self.__halo, self.__radius, self.__peak_mass_index).access()

    #     exsitu_by_peak_mass_index = exsitu_particles_data(self.__output_file_path,
    #                                                       self.__list_directory,
    #                                                       self.__snap_num,
    #                                                       self.__part_type,
    #                                                       self.__halo,
    #                                                       self.__radius,
    #                                                       self.__peak_mass_index).access()

    #     tree, _ = merger_tree_data(self.__tree_directory, self.__snap_num).access()

    #     exsitu_merged_with_tree = pd.merge(exsitu_by_peak_mass_index[exsitu_by_peak_mass_index['PeakMassIndex'] == self.__peak_mass_index], tree, left_on='RootIndex', right_on='FirstProgenitor', how='inner')

    #     particles_grouped = exsitu_merged_with_tree[['BirthSnapshot', 'ParticleID']]
    #     particles_grouped = particles_grouped.groupby(['BirthSnapshot'])

    #     snapshots_grouped = {}

    #     for _, grouped in particles_grouped:
    #         # disc = data_access.snapshot_raw_as_dataframe.data(self.__output_file_path, birth_snapshot[0], self.__part_type).access()
    #         birth_snapshot = grouped['BirthSnapshot'].iloc[0]
    #         particles = grouped['ParticleID']

    #         for particle in particles:
    #             # print(f'For particle {particle}: BirthSnapshot {birth_snapshot}')
    #             particle_data = exsitu_merged_with_tree[exsitu_merged_with_tree['ParticleID'] == particle]

    #             descendant = particle_data['Descendant'].iloc[0]
    #             next_progenitor = particle_data['NextProgenitor'].iloc[0]

    #             # print(f'descendant = {descendant}; next_progenitor = {next_progenitor}')


    #             snapshots_grouped = self.navigate_tree(tree, particle, descendant, snapshots_grouped)

    #     print('snapshots_grouped')
    #     print(snapshots_grouped)
    #     print()
    #     print(snapshots_grouped['snapshot_251'])


    #     # birth_snapshot = particle_data['BirthSnapshot'].iloc[0]
    #     # birth_snapshots = exsitu_merged_with_tree['BirthSnapshot']

        
    #     # descendant = particle_data['Descendant'].iloc[0]
    #     # next_progenitor = particle_data['NextProgenitor'].iloc[0]

    #     descendants = exsitu_merged_with_tree['Descendant']
    #     next_progenitors = exsitu_merged_with_tree['NextProgenitor']

    #     # print()
    #     # print(f'descendant = {descendant}; next_progenitor = {next_progenitor}')
    #     # print()



    #     particle_mass = 0

    #     # disc = data_access.snapshot_raw_as_dataframe.data(self.__output_file_path, birth_snapshot, self.__part_type).access()


    #     # particle_data = disc[disc['ParticleID'] == particle]

    #     # print(f'Particle ID = {particle}')
    #     # print(particle_data)
    #     # print()

    #     # particle_mass += particle_data['Mass'].iloc[0]

    #     # print(f'Particle ID = {particle}')
    #     # print(f'particle_mass = {particle_mass}')
    #     # print()

    #     # count = 0

    #     # count = self.navigate_tree(tree, particle, descendant, count)

    #     # print()
    #     # print(f'{count} records')
    #     # print()

    # def navigate_tree(self, tree, particle, descendant, snapshots_grouped):
        
    #     particle_tree_record = tree[tree['FirstProgenitor'] == descendant]

    #     descendants = particle_tree_record['Descendant']
        
    #     if len(descendants) > 0:
    #         descendant = particle_tree_record['Descendant'].iloc[0]
    #         first_progenitor = particle_tree_record['FirstProgenitor'].iloc[0]
    #         next_progenitor = particle_tree_record['NextProgenitor'].iloc[0]
    #         tree_snapshot_number = particle_tree_record['SnapshotNumber'].iloc[0]
    #         birth_snapshot_number = tree_snapshot_number - 1

    #         birth_column = f'snapshot_{birth_snapshot_number}'
    #         tree_column = f'snapshot_{tree_snapshot_number}'

    #         # print(f'birth_column = {birth_column}; tree_column = {tree_column}')

    #         if tree_column in snapshots_grouped.keys():
    #             snapshots_grouped[tree_column].append(particle)
    #         else:
    #             snapshots_grouped[tree_column] = [particle]

    #         # tree_snapshot = data_access.snapshot_raw_as_dataframe.data(self.__output_file_path, tree_snapshot_number, self.__part_type).access()
    #         # birth_snapshot = data_access.snapshot_raw_as_dataframe.data(self.__output_file_path, birth_snapshot_number, self.__part_type).access()

    #         # print()
    #         # print(f'descendant = {descendant}; first_progenitor = {first_progenitor}; next_progenitor = {next_progenitor}; tree_snapshot_number = {tree_snapshot_number}; birth_snapshot_number = {birth_snapshot_number}')

    #         if descendant > -1:
    #             snapshots_grouped = self.navigate_tree(tree, particle, descendant, snapshots_grouped)

    #     return snapshots_grouped