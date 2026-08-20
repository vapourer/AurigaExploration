import data_access
from data_access import *

class data:
    def __init__(self, tree_file_path: str, snap_num: int) -> None:
        print('Generate subhalos_by_snapshot_from_merger_tree output')
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num

    def output(self):
        tree, _ = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()

        subhalos_per_snapshot = {}

        tree_length = len(tree)

        for i in range(tree_length):
            current_record = tree[tree.index == i]
            snapshot = current_record['SnapshotNumber'].iloc[0]
            subhalo = current_record['SubhaloNumber'].iloc[0]

            if snapshot in subhalos_per_snapshot.keys():
                subhalos_per_snapshot[snapshot].append(subhalo)
            else:
                subhalos_per_snapshot[snapshot] = [subhalo]

        print()

        for snapshot in subhalos_per_snapshot:
            subhalos = subhalos_per_snapshot[snapshot]
            unique_subhalos = set(subhalos)
            subhalo_count = len(unique_subhalos)
            print(f'snapshot {snapshot} has {subhalo_count} subhalos')

        print()

