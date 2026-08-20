import data_access
from data_access import *

class data:
    def __init__(self, tree_file_path: str, snap_num: int) -> None:
        print('Generate merger_tree_navigation_analysis output')
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num

    def output(self):
        tree, _ = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()



        first_progenitors = {}
        next_progenitors = {}
        descendants = {}
        
        tree_length = len(tree)

        for i in range(tree_length):

            current_first_progenitor = tree['FirstProgenitor'].iloc[i]

            if current_first_progenitor in first_progenitors.keys():
                count = first_progenitors[current_first_progenitor]
                count += 1
                first_progenitors[current_first_progenitor] = count
            else:
                first_progenitors[current_first_progenitor] = 1

            current_next_progenitor = tree['NextProgenitor'].iloc[i]

            if current_next_progenitor in next_progenitors.keys():
                count = next_progenitors[current_next_progenitor]
                count += 1
                next_progenitors[current_next_progenitor] = count
            else:
                next_progenitors[current_next_progenitor] = 1

            current_descendant = tree['Descendant'].iloc[i]

            if current_descendant in descendants.keys():

                # breakpoint()

                count = descendants[current_descendant]

                # breakpoint()

                count += 1
                descendants[current_descendant] = count
            else:
                descendants[current_descendant] = 1

        first_progenitors_count = 0
        
        print('first_progenitors')
        print('Key\t\tCount')
        
        for key in first_progenitors.keys():

            if first_progenitors[key] > 1:
                first_progenitors_count += 1
                print(f'{key}\t\t{first_progenitors[key]}')

        print()

        breakpoint()

        next_progenitors_count = 0

        print('next_progenitors')
        print('Key\t\tCount')
        
        for key in next_progenitors.keys():

            if next_progenitors[key] > 1:
                next_progenitors_count += 1
                print(f'{key}\t\t{next_progenitors[key]}')

        print()

        breakpoint()

        descendants_counts = {}

        descendants_count = 0

        print('descendants')
        print('Key\t\tCount')

        max_progenitors = 0
        
        for key in descendants.keys():

            if descendants[key] > 1:
                descendants_count += 1
                print(f'{key}\t\t{descendants[key]}')

                descendants_counts_key = descendants[key]

                if descendants_counts_key in descendants_counts.keys():
                    count = descendants_counts[descendants_counts_key]
                    count += 1
                    descendants_counts[descendants_counts_key] = count
                else:
                    descendants_counts[descendants_counts_key] = 1

            if descendants[key] == 37:
                max_progenitors = key

        print()

        print(f'first_progenitors_count = {first_progenitors_count}')
        print(f'next_progenitors_count = {next_progenitors_count}')
        print(f'descendants_count = {descendants_count}')

        print()
        print(f'Count of descendants with value = -1: {descendants[-1]}')

        print()
        print('descendants_counts')
        print(descendants_counts)
        print()

        print(f'{max_progenitors} has 37 progenitors')
        print()

