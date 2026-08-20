import numpy as np
import pandas as pd
from .disc_specify_radius import data as disc_data
from .starparticle_mergertree import data as starparticle_mergertree_data
from .merger_tree_as_dataframe import data as merger_tree_as_dataframe_data
import auriga_public.auriga_public as ap

class data:
    text = []

    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 tree_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: int,
                 radius: float,                 
                 peak_mass_index: int) -> None:
        
        print('Access merger_tree_back_to_particles data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index        

    def access(self):

        bounded_disc, _, _, _, _, _ = disc_data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        _, exsitu = starparticle_mergertree_data(self.__list_directory, self.__snap_num, self.__halo).access()
        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(bounded_disc['ParticleID']))
        reduced_exsitu = exsitu[(exsitu["ParticleID"].isin(reduced_disc_exsitu_particles)) & (exsitu['AccretedFlag'] == 0)]

        tree, tree_original = merger_tree_as_dataframe_data(self.__tree_directory, self.__snap_num).access()

        search_tree = tree[["SubhaloNumber", 'SnapshotNumber', "FirstProgenitor", "NextProgenitor", "Descendant",
                            'Redshift', 'Time', 'StellarMass', 'GasMass', 'TracerMass', 'StellarHalfMassRadius',
                            'GasHalfMassRadius', 'TracerHalfMassRadius']]

        reduced_exsitu_indexed = reduced_exsitu[reduced_exsitu['PeakMassIndex'] == self.__peak_mass_index]
        birth_subhalo_numbers = set(reduced_exsitu_indexed['BirthSubhaloIndex'])    

        print(f'reduced_exsitu_indexed has {len(reduced_exsitu_indexed)} records')
        print(reduced_exsitu_indexed)
        print()
        # reduced_exsitu_indexed.to_csv(f'./output/halo_6/merger_tree_subhalo_search/back_to_particles/ReducedExsituIndexed_{self.__snap_num}_{self.__peak_mass_index}.csv', index=False)


        search_tree_indexed = search_tree[search_tree['SubhaloNumber'].isin(birth_subhalo_numbers)]
        search_tree_indexed = search_tree_indexed.sort_values(['SnapshotNumber', 'SubhaloNumber'], ascending=False)

        print(f'search_tree_indexed has {len(search_tree_indexed)} records')
        print(search_tree_indexed)
        print()

        search_tree_indexed = pd.merge(search_tree_indexed, reduced_exsitu_indexed, left_on='FirstProgenitor', right_on='RootIndex', how='inner')
        # print(f'merged has {len(merged)} records')
        # print(merged)
        # print()
        # merged.to_csv(f'./output/halo_6/merger_tree_subhalo_search/back_to_particles/Merged_{self.__snap_num}_{self.__peak_mass_index}.csv', index=False)

        reduced_exsitu_indexed_unique = set(reduced_exsitu_indexed["RootIndex"])
        reduced_exsitu_indexed_unique = list(reduced_exsitu_indexed_unique)
        reduced_exsitu_indexed_unique.sort()

        initial_merges = list(search_tree_indexed.loc[search_tree_indexed["NextProgenitor"] != -1, "NextProgenitor"])
        search_tree_indexed = self.__list_merge_history(tree_original, initial_merges, search_tree_indexed)

        search_tree_indexed = self.__list_merge_history(tree_original, reduced_exsitu_indexed_unique, search_tree_indexed)
        search_tree_indexed = search_tree_indexed.sort_values(['SubhaloNumber', 'SnapshotNumber'], ascending=False)

        snapshot_number = [int(x) for x in search_tree_indexed['SnapshotNumber']]
        subhalo_number = [int(x) for x in search_tree_indexed['SubhaloNumber']]
        first_progenitor = [int(x) for x in search_tree_indexed['FirstProgenitor']]
        next_progenitor = [int(x) for x in search_tree_indexed['NextProgenitor']]
        descendant = [int(x) for x in search_tree_indexed['Descendant']]

        search_tree_indexed['SnapshotNumber'] = snapshot_number
        search_tree_indexed['SubhaloNumber'] = subhalo_number
        search_tree_indexed['FirstProgenitor'] = first_progenitor
        search_tree_indexed['NextProgenitor'] = next_progenitor
        search_tree_indexed['Descendant'] = descendant

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)

        # print()
        # print(f'birth_subhalo_numbers ({len(birth_subhalo_numbers)})')
        # print(birth_subhalo_numbers)
        # print()
            
        return search_tree_indexed

    def __list_merge_history(self, tree, indices, search_tree):
        
        record_count = len(indices)

        empty = {'SnapshotNumber': [], 'FirstProgenitor': [], 'NextProgenitor': [], 'Descendant': [],
                 'Redshift': [], 'Time': [], 'SubhaloNumber': [], 'StellarMass': [], 'GasMass': [],
                 'TracerMass': [], 'StellarHalfMassRadius': [], 'GasHalfMassRadius': [],
                 'TracerHalfMassRadius': []}
            
        search_result = pd.DataFrame(empty)

        merge_count = 0
        merges = []

        history_record_count = 0

        fields = ["SubhaloNumber", 'SnapNum', "FirstProgenitor", "NextProgenitor", "Descendant", 'Redshift',
                  'Time', 'SubhaloMassType', 'SubhaloHalfmassRadType']

        for i in range(record_count):
            
            root_index = indices[i]
            history = tree.GetObjectHistoryFromMergerTreeObjectID(root_index, fields)

            stellar_mass = []
            gas_mass = []
            tracer_mass = []

            stellar_half_mass_radius = []
            gas_half_mass_radius = []
            tracer_half_mass_radius = []

            history_record_count = len(history['SubhaloNumber'])

            for j in range(history_record_count):
                stellar_mass.append(history['SubhaloMassType'][j][4])
                gas_mass.append(history['SubhaloMassType'][j][0])
                tracer_mass.append(history['SubhaloMassType'][j][6])
                stellar_half_mass_radius.append(history['SubhaloHalfmassRadType'][j][4])
                gas_half_mass_radius.append(history['SubhaloHalfmassRadType'][j][0])
                tracer_half_mass_radius.append(history['SubhaloHalfmassRadType'][j][6])
                
            data_structure = {'SnapshotNumber': history["SnapNum"], 'FirstProgenitor': history["FirstProgenitor"],
                              'NextProgenitor': history["NextProgenitor"], 'Descendant': history["Descendant"], 'Redshift': history["Redshift"],
                              'Time': history["Time"], 'SubhaloNumber': history["SubhaloNumber"], 'StellarMass': stellar_mass,
                              'GasMass': gas_mass, 'TracerMass': tracer_mass, 'StellarHalfMassRadius': stellar_half_mass_radius,
                              'GasHalfMassRadius': gas_half_mass_radius, 'TracerHalfMassRadius': tracer_half_mass_radius}
                
            search_result = pd.concat([search_result, pd.DataFrame(data_structure)])
            data.text.append(f'search_result for {root_index}: {len(search_result)} records\n')
                
            merges += list(search_result.loc[search_result["NextProgenitor"] != -1, "NextProgenitor"])
            merge_count = len(merges)

        search_tree = pd.concat([search_tree, search_result])

        merges_unique = list(set((merges)))
        merges_unique = [int(x) for x in merges_unique]
        merges_unique.sort()

        if merge_count > 0:
            search_tree = self.__list_merge_history(tree, merges_unique, search_tree)

        return search_tree
