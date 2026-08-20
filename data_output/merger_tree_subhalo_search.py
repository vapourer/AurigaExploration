import numpy as np
import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self, output_file_path: str, list_file_path: str, tree_file_path: str, snap_num: int, part_type: int, radius: float) -> None:
        print('Generate merger_tree_subhalo_search output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__radius = radius
        self.__halo = 'halo_6'   

    def output(self) -> None:

        # peak_mass_indices = np.array([36275, 37138, 37333, 36900, 377, 188717, 23050, 135236, 190063, 918])
        peak_mass_indices = np.array([918])

        bounded_disc, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        _, exsitu = data_access.starparticle_mergertree.data(self.__list_directory, self.__snap_num, self.__halo).access()

        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(bounded_disc['ParticleID']))
        reduced_exsitu = exsitu[(exsitu["ParticleID"].isin(reduced_disc_exsitu_particles)) & (exsitu['AccretedFlag'] == 0)]

        tree, tree_original = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()
        search_tree = tree[["SubhaloNumber", 'SnapshotNumber', "FirstProgenitor", "NextProgenitor", "Descendant"]]

        for index in peak_mass_indices:

            reduced_exsitu_indexed = reduced_exsitu[reduced_exsitu['PeakMassIndex'] == index]
            birth_subhalo_numbers = set(reduced_exsitu_indexed['BirthSubhaloIndex'])

            search_tree_indexed = search_tree[search_tree['SubhaloNumber'].isin(birth_subhalo_numbers)]
            search_tree_indexed = search_tree_indexed.sort_values(['SnapshotNumber', 'SubhaloNumber'], ascending=False)

            reduced_exsitu_indexed_unique = set(reduced_exsitu_indexed["RootIndex"])
            reduced_exsitu_indexed_unique = list(reduced_exsitu_indexed_unique)
            reduced_exsitu_indexed_unique.sort()

            header = 'PeakMassIndex,'
            header += 'RootIndex,'
            header += 'SubhaloNumber,'
            header += 'SnapshotNumber,'
            header += 'FirstProgenitor,'
            header += 'NextProgenitor,'
            header += 'Descendant\n'

            records = [header]

            record_count = len(search_tree_indexed["SubhaloNumber"])
            
            for j in range(record_count):
                record = f'{index},'
                record += f'{-1},' # temporary - adjust after reintegrating exsitu fields
                record += f'{search_tree_indexed["SubhaloNumber"].iloc[j]},'
                record += f'{search_tree_indexed["SnapshotNumber"].iloc[j]},'
                record += f'{search_tree_indexed["FirstProgenitor"].iloc[j]},'
                record += f'{search_tree_indexed["NextProgenitor"].iloc[j]},'
                record += f'{search_tree_indexed["Descendant"].iloc[j]}\n'
                records.append(record)

            records = self.__list_merge_history(tree_original, index, reduced_exsitu_indexed_unique, records)
            
            with open(f'./output/halo_6/merger_tree_subhalo_search/MergerTreeSubhaloSearch_{self.__snap_num}_{index}.csv', 'w') as file:
                file.writelines(records)

    def __list_merge_history(self, tree, peak_mass_index, indices, records):
        
        record_count = len(indices)

        merge_count = 0
        merges = []

        fields = ["SubhaloNumber", 'SnapNum', "FirstProgenitor", "NextProgenitor", "Descendant"]

        for i in range(record_count):
        
            root_index = indices[i]
            history = tree.GetObjectHistoryFromMergerTreeObjectID(root_index, fields)            
            history_count = len(history["SubhaloNumber"])

            for j in range(history_count):
                record = f'{peak_mass_index},'
                record += f'{root_index},'
                record += f'{history["SubhaloNumber"][j]},'
                record += f'{history["SnapNum"][j]},'
                record += f'{history["FirstProgenitor"][j]},'
                record += f'{history["NextProgenitor"][j]},'
                record += f'{history["Descendant"][j]}\n'
                records.append(record)

                if history["NextProgenitor"][j] != -1:
                    merges.append(history["NextProgenitor"][j])
                    merge_count += 1

        merges_unique = set(merges)
        merges_unique = list(merges_unique)
        merges_unique.sort()

        if merge_count > 0:
            self.__list_merge_history(tree, peak_mass_index, merges_unique, records)

        return records
