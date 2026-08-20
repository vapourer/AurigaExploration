import data_access
from data_access import *

class data:
    def __init__(self, tree_file_path: str, snap_num: int) -> None:
        print('Generate merger_tree output')
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num

    def output(self) -> None:
        tree = data_access.merger_tree.data(self.__tree_directory, self.__snap_num).access()

        print()
        print('Array sizes')
        print(f'Descendant: {len(tree.data["Descendant"])}; unique: {len(tree.data["Descendant"]) == len(set(tree.data["Descendant"]))}')
        print(f'FirstProgenitor: {len(tree.data["FirstProgenitor"])}; unique: {len(tree.data["FirstProgenitor"]) == len(set(tree.data["FirstProgenitor"]))}')
        print(f'NextProgenitor: {len(tree.data["NextProgenitor"])}; unique: {len(tree.data["NextProgenitor"]) == len(set(tree.data["NextProgenitor"]))}')
        print(f'FirstHaloInFOFGroup: {len(tree.data["FirstHaloInFOFGroup"])}; unique: {len(tree.data["FirstHaloInFOFGroup"]) == len(set(tree.data["FirstHaloInFOFGroup"]))}')
        print(f'NextHaloInFOFGroup: {len(tree.data["NextHaloInFOFGroup"])}; unique: {len(tree.data["NextHaloInFOFGroup"]) == len(set(tree.data["NextHaloInFOFGroup"]))}')
        print(f'Group_R_Crit200: {len(tree.data["Group_R_Crit200"])}; unique: {len(tree.data["Group_R_Crit200"]) == len(set(tree.data["Group_R_Crit200"]))}')
        print(f'SnapNum: {len(tree.data["SnapNum"])}; unique: {len(tree.data["SnapNum"]) == len(set(tree.data["SnapNum"]))}')
        print(f'SubhaloMassType: {len(tree.data["SubhaloMassType"])}')
        print('n.b. SubhaloMassType is an array of arrays, met previously when looking at the subhalo object and yet to explore properly.')
        print()

        print(f'SubhaloNumber: {len(tree.data["SubhaloNumber"])}')
        print(f'SubhaloNumber = 0: {len(tree.data["SubhaloNumber"][tree.data["SubhaloNumber"] == 0])}')
        print(f'FileNr: {len(tree.data["FileNr"])}')
        print(f'FileNr = 0: {len(tree.data["FileNr"][tree.data["FileNr"] == 0])}')
        print(f'SnapNum = 251: {len(tree.data["SnapNum"][tree.data["SnapNum"] == 251])}')
        print()

        print('SubhaloMassType')
        print('First record')
        print(f'Size = {len(tree.data["SubhaloMassType"][0])}')        
        print()

        print(f'{len(set(tree.data["SnapNum"]))} unique SnapNum')
        print()

        # print('Merger tree data')
        # print(tree.data)
        # print()

        if self.__snap_num < 10:
            three_digit = '00' + str(self.__snap_num)
        elif self.__snap_num >= 10 and self.__snap_num < 100:
            three_digit = '0' + str(self.__snap_num)
        else:
            three_digit = str(self.__snap_num)

        header = 'Index,'
        header += 'SnapNum,'
        header += 'FirstProgenitor,'
        header += 'NextProgenitor,'
        header += 'Descendant,'
        header += 'Redshift,'
        header += 'Time,'
        header += 'SubhaloNumber,'
        header += 'StellarMass,'
        header += 'GasMass,'
        header += 'TracerMass\n'
        
        records = [header]
        record_count = len(tree.data["SnapNum"])

        for i in range(record_count):
            record = f'{str(i)},'
            record += f'{tree.data["SnapNum"][i]},'
            record += f'{tree.data["FirstProgenitor"][i]},'
            record += f'{tree.data["NextProgenitor"][i]},'
            record += f'{tree.data["Descendant"][i]},'
            record += f'{tree.data["Redshift"][i]},'
            record += f'{tree.data["Time"][i]},'
            record += f'{tree.data["SubhaloNumber"][i]},'
            record += f'{tree.data["SubhaloMassType"][i][4]},'
            record += f'{tree.data["SubhaloMassType"][i][0]},'
            record += f'{tree.data["SubhaloMassType"][i][6]}\n'
            records.append(record)                

        with open(f'./output/halo_6/merger_trees/MergerTree_{three_digit}.csv', 'w') as file:
            file.writelines(records)

        print()

        unique_subhalo_count = set(tree.data["SubhaloNumber"])
        print(f'{len(unique_subhalo_count)} unique subhalos')