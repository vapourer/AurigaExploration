import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self, output_file_path: str, list_file_path: str, tree_file_path: str, snap_num: int, part_type: int, halo: str, radius: float, peak_mass_index: int) -> None:
        print('Generate starparticle_mergertree_comparison output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__radius = radius
        self.__halo = halo
        self.__peak_mass_index = peak_mass_index

    def output(self) -> None:
        bounded_disc, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        _, exsitu = data_access.starparticle_mergertree.data(self.__list_directory, self.__snap_num, self.__halo).access()

        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(bounded_disc['ParticleID']))
        bounded_disc_exsitu = bounded_disc[bounded_disc['ParticleID'].isin(reduced_disc_exsitu_particles)]
        reduced_exsitu = exsitu[(exsitu["ParticleID"].isin(reduced_disc_exsitu_particles)) & (exsitu['AccretedFlag'] == 0)]
        other_exsitu = exsitu[(exsitu["ParticleID"].isin(reduced_disc_exsitu_particles)) & (exsitu['AccretedFlag'] == 1)]

        tree, _ = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()

        bounded_disc_exsitu_merged = pd.merge(bounded_disc_exsitu, reduced_exsitu, on='ParticleID', how='inner')
        bounded_disc_exsitu_merged_left = pd.merge(bounded_disc_exsitu, reduced_exsitu, on='ParticleID', how='left', suffixes=('_disc', '_exsitu'))
        bounded_disc_exsitu_merged_right = pd.merge(bounded_disc_exsitu, reduced_exsitu, on='ParticleID', how='right')
        other_bounded_disc_exsitu_merged = pd.merge(bounded_disc_exsitu, other_exsitu, on='ParticleID', how='inner')

        print()
        print(f'Mergertree: length = {len(tree)}; FirstProgenitor field unique = {tree["FirstProgenitor"].is_unique}')
        print(tree)
        print()

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)

        grouped = exsitu[['BirthSubhaloIndex', 'ParticleID']]
        grouped = grouped.groupby(['BirthSubhaloIndex']).count()

        print('ParticleIDs grouped by BirthSubhaloIndex')
        # print(grouped)
        # print()
        print(f'{len(grouped)} records')
        print()

        common = set(exsitu["BirthSubhaloIndex"]).intersection(set(tree['SubhaloNumber']))
        print(f'common: {len(common)} records')
        print()

        print(f'bounded_disc: {len(bounded_disc)} records')
        # print(bounded_disc)
        print()

        print(f'exsitu: {len(exsitu)} records')
        # print(exsitu)
        print()

        print(f'bounded_disc_exsitu: {len(bounded_disc_exsitu)} records')
        # print(bounded_disc_exsitu)
        print()

        print(f'bounded_disc_exsitu_merged: {len(bounded_disc_exsitu_merged)} records')
        # print(bounded_disc_exsitu_merged)
        print()

        print(f'bounded_disc_exsitu_merged_left: {len(bounded_disc_exsitu_merged_left)} records')
        print(bounded_disc_exsitu_merged_left)
        print()

        print(f'bounded_disc_exsitu_merged_right: {len(bounded_disc_exsitu_merged_right)} records')
        # print(bounded_disc_exsitu_merged_right)
        print()

        bounded_disc_exsitu_merged_left_only = bounded_disc_exsitu_merged_left[pd.isna(bounded_disc_exsitu_merged_left['PeakMassIndex'])]
        print(bounded_disc_exsitu_merged_left_only.columns)
        print(f'bounded_disc_exsitu_merged_left_only: {len(bounded_disc_exsitu_merged_left_only)} records')
        print(bounded_disc_exsitu_merged_left_only['ParticleID'])
        print()

        missing_particles = bounded_disc_exsitu_merged_left_only['ParticleID']
        print(f'Are any missing particles in original exsitu? exsitu has {len(exsitu[exsitu["ParticleID"].isin(missing_particles)])} of them') 

        exsitu_missing_particles = exsitu[exsitu["ParticleID"].isin(missing_particles)]
        print('exsitu_missing_particles')
        print(exsitu_missing_particles)
        print()

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)

        # print('bounded_disc_exsitu_merged')
        # grouped = bounded_disc_exsitu_merged[['PeakMassIndex', 'ParticleID']]
        # print(grouped.groupby(['PeakMassIndex']).count())
        # print()

        # print('other_bounded_disc_exsitu_merged')
        # grouped = other_bounded_disc_exsitu_merged[['PeakMassIndex', 'ParticleID']]
        # print(grouped.groupby(['PeakMassIndex']).count())
        # print()

        # print(f'Mergertree SubhaloNumber: {len(set(tree["SubhaloNumber"]))} records')
        # # print(tree["SubhaloNumber"])
        # print()

        bounded_disc_exsitu_merged_with_tree = pd.merge(bounded_disc_exsitu_merged[bounded_disc_exsitu_merged['PeakMassIndex'] == self.__peak_mass_index],
                                                        tree, left_on='RootIndex', right_on='FirstProgenitor', how='inner')
        print(f'bounded_disc_exsitu_merged_with_tree ({len(bounded_disc_exsitu_merged_with_tree)})')
        # print(bounded_disc_exsitu_merged_with_tree)
        print()

        # bounded_disc_exsitu_merged_with_tree.to_csv(f'./output/halo_6/combined_datasets/DataComparisonByPeakMassIndex_{self.__snap_num}_{self.__peak_mass_index}.csv', index=False)

        # print('bounded_disc_exsitu_merged')
        # grouped = bounded_disc_exsitu_merged[['RootIndex', 'ParticleID']]
        # grouped = grouped.groupby(['RootIndex']).count()
        # print(grouped)
        # print()

        # grouped.to_csv(f'./output/halo_6/combined_datasets/BoundedDiscExsituMergedGroupByRootIndex_{self.__snap_num}_{self.__peak_mass_index}.csv', index=True)

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)
        
        print(f'bounded_disc_exsitu_merged_with_tree ({len(bounded_disc_exsitu_merged_with_tree)} records)')
        grouped = bounded_disc_exsitu_merged_with_tree[['RootIndex', 'ParticleID']]
        grouped = grouped.groupby(['RootIndex']).count()
        # grouped = grouped.groupby(['RootIndex'])
        print(grouped)
        print()

        # for _, group in grouped:
        #     print(group)

        # print(f'tree ({len(tree)} records)')
        # grouped = tree[['FirstProgenitor', 'SnapshotNumber']]
        # grouped = grouped.groupby(['FirstProgenitor']).count()
        # # print(grouped)
        print()

        # grouped.to_csv(f'./output/halo_6/combined_datasets/TreeGroupByFirstProgenitor_{self.__snap_num}_{self.__peak_mass_index}.csv', index=True)
