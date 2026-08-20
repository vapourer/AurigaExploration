import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self, list_file_path: str, snap_num: int, halo: str) -> None:
        print('Generate starparticle_mergertree output')
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__halo = halo

    def output(self) -> None:
        insitu, exsitu = data_access.starparticle_mergertree.data(self.__list_directory, self.__snap_num, self.__halo).access()

        print('Merger tree data')
        print(exsitu)
        print()
        print(f'Insitu ParticleIDs ({len(insitu["ParticleID"])})')
        print()

        print(f'Exsitu ParticleIDs ({len(exsitu["ParticleID"])})')
        print(f'Exsitu PeakMassIndex ({len(exsitu["PeakMassIndex"])})')
        print()
        
        print(f'{len(set(exsitu["ParticleID"]))} unique ParticleIDs')
        print(f'{len(set(exsitu["PeakMassIndex"]))} unique PeakMassIndex')
        print()

        print(f'BirthSubhaloIndex: MIN = {min(exsitu["BirthSubhaloIndex"])}; MAX = {max(exsitu["BirthSubhaloIndex"])}')
        print(f'BirthSubhaloIndex: count = {len(set(exsitu["BirthSubhaloIndex"]))}')
        print()

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)

        grouped = exsitu[['BirthSubhaloIndex', 'ParticleID']]
        grouped = grouped.groupby(['BirthSubhaloIndex']).count()

        print('ParticleIDs grouped by BirthSubhaloIndex')
        print(grouped)
        print()

        print(str(135236))
        print(f'{exsitu[exsitu["PeakMassIndex"] == 135236]}')
        print()

        # birth_subhalo_index_unique = set(exsitu["BirthSubhaloIndex"])
        # subhalo_number_unique = set()