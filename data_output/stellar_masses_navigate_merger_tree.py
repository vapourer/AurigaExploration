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
        
        print('Generate stellar_masses_navigate_merger_tree output')        
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
        # particles = exsitu_merged_with_tree['ParticleID']
        root_indices = set(exsitu_merged_with_tree['RootIndex'])

        snapshots_grouped = {}

        # for particle in particles:
        for root_index in root_indices:
                
            # particle_data = exsitu_merged_with_tree[exsitu_merged_with_tree['ParticleID'] == particle]
            # snapshots_grouped[particle_data['SnapshotNumber'].iloc[0]] = [(particle_data['SubhaloNumber'].iloc[0], particle)]

            # descendant = particle_data['Descendant'].iloc[0]

            tree_record = tree[tree['FirstProgenitor'] == root_index]
            descendant = tree_record['Descendant'].iloc[0]
            
            snapshots_grouped = self.navigate_tree(tree, descendant, snapshots_grouped)
        
        print()

        counter = 0

        # print(f'snapshots_grouped: 251 ({len(snapshots_grouped[251])})')        
        # # print(snapshots_grouped[251])
        # print()

        # print(f'snapshots_grouped: 31 ({len(snapshots_grouped[31])})')        
        # print(snapshots_grouped[31])
        # print()

        snapshots_grouped = {k: v for k, v in sorted(snapshots_grouped.items(), key=lambda item: item[0])}

        snapshot_number = []
        subhalo_index = []
        stellar_mass = []
        gas_mass = []
        redshift = []
        time = []
        stellar_half_mass_radius = []
        dwarf = []
        greater_than_dwarf = []

        for snapshot in snapshots_grouped.keys():

            subhalos = []

            for each_snapshot in snapshots_grouped[snapshot]:
                subhalos.append(each_snapshot[0])

            unique_subhalos = set(subhalos)

            # if len(unique_subhalos) > 1:
            #     counter += 1
            #     print(f'{snapshot}\t{snapshots_grouped[snapshot][0]}; has {len(unique_subhalos)} discrete values')

            #     for subhalo in unique_subhalos:
            #         print(f'\t\t{subhalo}')

            #     print()
            #     print(f'\t\t{snapshots_grouped[snapshot]}')
            #     print()
            # else:
            #     print(f'{snapshot}\t{snapshots_grouped[snapshot][0]}')

            for subhalo in unique_subhalos:
                snapshot_number.append(snapshot)
                subhalo_index.append(subhalo)

                record = [tuple for tuple in snapshots_grouped[snapshot] if tuple[0] == subhalo]

                stellar_mass.append(record[0][1])
                gas_mass.append(record[0][2])
                redshift.append(record[0][3])
                time.append(record[0][4])
                stellar_half_mass_radius.append(record[0][5])
                dwarf.append(record[0][6])
                greater_than_dwarf.append(record[0][7])

                # print(record)

        # print()

        # print(f'counter = {counter}')
        # print()

        data_structure = {'SnapshotNumber': snapshot_number,
                          'SubhaloNumber': subhalo_index,
                          'StellarMass': stellar_mass,
                          'GasMass': gas_mass,
                          'Redshift': redshift,
                          'Time': time,
                          'StellarHalfMassRadius': stellar_half_mass_radius,
                          'DwarfGalaxy': dwarf,
                          'GreaterThanDwarf': greater_than_dwarf}
        
        data_frame = pd.DataFrame(data_structure)

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)

        # print()
        # print(data_frame)
        # print()

        data_frame.to_csv(f'./output/halo_6/stellar_mass_histories/StellarMassHistory_{self.__snap_num}_{self.__peak_mass_index}.csv')

    def navigate_tree(self, tree, descendant, snapshots_grouped):

        h = 0.6777

        tree_record = tree[tree.index == descendant]

        descendants = tree_record['Descendant']
        
        if len(descendants) > 0:

            descendant = tree_record['Descendant'].iloc[0]
            tree_snapshot_number = tree_record['SnapshotNumber'].iloc[0]
            subhalo_index = tree_record['SubhaloNumber'].iloc[0]
            stellar_mass = tree_record['StellarMass'].iloc[0] * (10**10) / h
            gas_mass = tree_record['GasMass'].iloc[0] * (10**10) / h
            # first_progenitor = tree_record['FirstProgenitor'].iloc[0]
            # next_progenitor = tree_record['NextProgenitor'].iloc[0]
            redshift = tree_record['Redshift'].iloc[0]
            time = tree_record['Time'].iloc[0]
            stellar_half_mass_radius = tree_record['StellarHalfMassRadius'].iloc[0]  

            # stellar_mass_compare = stellar_mass * (10**10) / h
            dwarf = False

            if stellar_mass >= 10**7 and stellar_mass < 10**9:
                dwarf = True

            greater_than_dwarf = False
            
            if stellar_mass >= 10**9:
                greater_than_dwarf = True

            if tree_snapshot_number in snapshots_grouped.keys():
                # snapshots_grouped[tree_snapshot_number].append((subhalo_index, stellar_mass, descendant, first_progenitor, next_progenitor))
                snapshots_grouped[tree_snapshot_number].append((subhalo_index, stellar_mass, gas_mass, redshift, time, stellar_half_mass_radius, dwarf, greater_than_dwarf))
            else:
                # snapshots_grouped[tree_snapshot_number] = [(subhalo_index, stellar_mass, descendant, first_progenitor, next_progenitor)]
                snapshots_grouped[tree_snapshot_number] = [(subhalo_index, stellar_mass, gas_mass, redshift, time, stellar_half_mass_radius, dwarf, greater_than_dwarf)]

            if descendant > -1:
                snapshots_grouped = self.navigate_tree(tree, descendant, snapshots_grouped)

        return snapshots_groupedstellar_mass_histories