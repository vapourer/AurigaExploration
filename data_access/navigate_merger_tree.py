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
        
        print('Access navigate_merger_tree data')        
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
        root_indices = set(exsitu_merged_with_tree['RootIndex'])

        snapshots_grouped = {}

        for root_index in root_indices:

            tree_record = tree[tree['FirstProgenitor'] == root_index]
            descendant = tree_record['Descendant'].iloc[0]
            
            snapshots_grouped = self.navigate_tree(tree, descendant, snapshots_grouped)

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

        return data_frame, snapshots_grouped.keys()

    def navigate_tree(self, tree, descendant, snapshots_grouped):

        h = 0.6777

        tree_record = tree[tree.index == descendant]

        descendants = tree_record['Descendant']
        
        if len(descendants) > 0:

            descendant = tree_record['Descendant'].iloc[0]
            tree_snapshot_number = tree_record['SnapshotNumber'].iloc[0]
            subhalo_index = tree_record['SubhaloNumber'].iloc[0]
            stellar_mass = tree_record['StellarMass'].iloc[0]
            gas_mass = tree_record['GasMass'].iloc[0]
            redshift = tree_record['Redshift'].iloc[0]
            time = tree_record['Time'].iloc[0]
            stellar_half_mass_radius = tree_record['StellarHalfMassRadius'].iloc[0]  

            stellar_mass_compare = stellar_mass * (10**10) / h
            dwarf = False

            if stellar_mass_compare >= 10**7 and stellar_mass_compare < 10**9:
                dwarf = True

            greater_than_dwarf = False
            
            if stellar_mass_compare >= 10**9:
                greater_than_dwarf = True

            if tree_snapshot_number in snapshots_grouped.keys():
                snapshots_grouped[tree_snapshot_number].append((subhalo_index, stellar_mass, gas_mass, redshift, time, stellar_half_mass_radius, dwarf, greater_than_dwarf))
            else:
                snapshots_grouped[tree_snapshot_number] = [(subhalo_index, stellar_mass, gas_mass, redshift, time, stellar_half_mass_radius, dwarf, greater_than_dwarf)]

            if descendant > -1:
                snapshots_grouped = self.navigate_tree(tree, descendant, snapshots_grouped)

        return snapshots_grouped