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
        
        print('Generate particle_history output')
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

        tree, _ = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()

        exsitu_merged_with_tree = pd.merge(exsitu_by_peak_mass_index[exsitu_by_peak_mass_index['PeakMassIndex'] == self.__peak_mass_index], tree, left_on='RootIndex', right_on='FirstProgenitor', how='inner')

        particles_grouped = exsitu_merged_with_tree[['BirthSnapshot', 'ParticleID']]
        particles_grouped = particles_grouped.groupby(['BirthSnapshot'])

        lines = []

        for _, grouped in particles_grouped:
            
            birth_snapshot = grouped['BirthSnapshot'].iloc[0]
            particles = grouped['ParticleID']

            for particle in particles:

                lines.append(f'For particle {particle}: BirthSnapshot {birth_snapshot}\n')
                print(f'For particle {particle}: BirthSnapshot {birth_snapshot}')

                particle_data = exsitu_merged_with_tree[exsitu_merged_with_tree['ParticleID'] == particle]

                descendant = particle_data['Descendant'].iloc[0]
                next_progenitor = particle_data['NextProgenitor'].iloc[0]

                lines.append(f'descendant = {descendant}; next_progenitor = {next_progenitor}\n')
                print(f'descendant = {descendant}; next_progenitor = {next_progenitor}')

                count = 0
                count, lines = self.navigate_tree(tree, particle, descendant, count, lines)

                lines.append(f'{count} records\n\n')
                print(f'{count} records')
                
            print(f'Completed for BirthSnapshot {birth_snapshot}')
            print()

        with open(f'./output/halo_6/merger_tree_subhalo_search/back_to_particles/MergerTreeByBirthSubhaloIndex_{self.__peak_mass_index}.txt', 'w') as file:
            file.writelines(lines)

    def navigate_tree(self, tree, particle, descendant, count, lines):

        count += 1

        particle_tree_record = tree[tree['FirstProgenitor'] == descendant]
        descendants = particle_tree_record['Descendant']
        
        if len(descendants) > 0:
            descendant = particle_tree_record['Descendant'].iloc[0]
            first_progenitor = particle_tree_record['FirstProgenitor'].iloc[0]
            next_progenitor = particle_tree_record['NextProgenitor'].iloc[0]
            tree_snapshot_number = particle_tree_record['SnapshotNumber'].iloc[0]
            birth_snapshot_number = tree_snapshot_number - 1

            lines.append(f'descendant = {descendant}; first_progenitor = {first_progenitor}; next_progenitor = {next_progenitor}; tree_snapshot_number = {tree_snapshot_number}; birth_snapshot_number = {birth_snapshot_number}\n')
            print(f'descendant = {descendant}; first_progenitor = {first_progenitor}; next_progenitor = {next_progenitor}; tree_snapshot_number = {tree_snapshot_number}; birth_snapshot_number = {birth_snapshot_number}')

            if descendant > -1:
                count, lines = self.navigate_tree(tree, particle, descendant, count, lines)

        return count, lines
